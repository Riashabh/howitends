import { useEffect, useState } from "react";

interface ApiResponse {
  message: string;
}

// Define the shape of a movie item
interface MovieItem {
  id: number;
  title: string;
  year?: string;
  poster_url: string;
}

function App() {
  const [data, setData] = useState<ApiResponse | null>(null);
  // Use the MovieItem interface for better type safety
  const [results, setResults] = useState<MovieItem[]>([]);
  const [endings, setEndings] = useState<Record<number, string>>({});

  // 1. Check backend connection
  useEffect(() => {
    async function load() {
      try {
        const res = await fetch("http://127.0.0.1:8000/");
        const json = await res.json();
        setData(json);
      } catch (err) {
        console.error("Failed to connect to backend:", err);
        setData({ message: "Error: Could not connect to backend." });
      }
    }
    load();
  }, []);

  // 2. Search movies
  async function handleSearch(query: string) {
    try {
      const res = await fetch(`http://127.0.0.1:8000/search?q=${query}`);
      const json = await res.json();
      setResults(json.results);
      // Clear old endings on new search
      setEndings({});
    } catch (err) {
      console.error("Search failed:", err);
    }
  }

  // 3. Get ending classification
  console.log("handleCheckEnding loaded");

  async function handleCheckEnding(title: string, year: string | undefined, id: number) {
    // Prevent re-fetching if already loading or fetched
    if (endings[id] && endings[id] !== 'Error finding ending') {
      console.log('Ending already fetched or is being fetched.');
      return;
    }

    console.log("→ sending request:", title, year);

    try {
      // SET LOADING STATE for immediate user feedback
      setEndings((prev) => ({ ...prev, [id]: 'loading...' }));

      const res = await fetch("http://127.0.0.1:8000/check-ending", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, year }),
      });

      console.log("status:", res.status);

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`API request failed with status ${res.status}: ${errorText}`);
      }

      const json = await res.json();

      // store result for the clicked movie
      setEndings((prev) => ({ ...prev, [id]: json.ending }));
    } catch (err) {
      console.error("fetch failed:", err);
      // SET ERROR STATE for user feedback
      setEndings((prev) => ({ ...prev, [id]: 'Error finding ending' }));
    }
  }

  return (
    <div className="p-6 bg-gray-50 min-h-screen font-sans">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-4 text-center text-gray-800">
          {data ? data.message : "Connecting..."}
        </h1>

        {/* Search bar */}
        <div className="mb-6 flex justify-center">
          <input
            type="text"
            placeholder="Search movie or series..."
            onKeyDown={(e) => {
              if (e.key === "Enter")
                handleSearch((e.target as HTMLInputElement).value);
            }}
            className="border p-3 rounded-lg w-full max-w-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Search results */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {results.map((item) => (
            // Added flex flex-col to make card layout easier
            <div key={item.id} className="text-center bg-white border rounded-lg shadow-md hover:shadow-lg transition-shadow overflow-hidden flex flex-col">
              {item.poster_url && (
                <img
                  src={item.poster_url}
                  alt={item.title}
                  onClick={() => handleCheckEnding(item.title, item.year, item.id)}
                  className="w-full h-64 object-cover rounded-t-lg cursor-pointer"
                />
              )}
              {/* Added p-4 and flex-grow to title to push ending to bottom */}
              <div className="p-4 flex flex-col flex-grow">
                <p className="mt-2 font-semibold flex-grow">
                  {item.title} {item.year && `(${item.year})`}
                </p>

                {/* *** THIS IS THE FIX ***
                  This block reads from the 'endings' state and displays
                  the correct ending (or loading/error) for THIS item.
                */}
                <div className="h-10 flex items-center justify-center mt-2">
                  {endings[item.id] && (
                    <p className="text-sm font-medium text-gray-700">
                      <strong>Ending:</strong> {endings[item.id]}
                    </p>
                  )}
                </div>
                {/* *** END OF FIX *** */}
              </div>
            </div>
          ))}
        </div>

        {/* This debug <pre> tag is no longer needed, as the data is now in the card */}
        {/* <pre>{JSON.stringify(endings, null, 2)}</pre> */}
      </div>
    </div>
  );
}

export default App;