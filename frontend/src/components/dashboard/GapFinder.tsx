import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import { Lightbulb, ChefHat, TrendingUp } from 'lucide-react'

export default function GapFinder() {
  const { data, isLoading } = useQuery({
    queryKey: ['gap-finder'],
    queryFn: async () => {
      const res = await axios.get('/api/gap-finder')
      return res.data
    },
    refetchInterval: 30000,
  })

  if (isLoading) {
    return (
      <div className="bg-white rounded-xl shadow-sm p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-6 bg-gray-200 rounded w-2/3"></div>
          <div className="h-20 bg-gray-200 rounded"></div>
        </div>
      </div>
    )
  }

  const suggestions = data?.suggestions || []
  const topSuggestion = suggestions[0]

  return (
    <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl shadow-sm p-6 border border-purple-100">
      <div className="flex items-center gap-3 mb-4">
        <Lightbulb className="w-6 h-6 text-purple-600" />
        <h2 className="text-xl font-bold text-gray-900">Smart Suggestions</h2>
      </div>

      {topSuggestion ? (
        <div className="space-y-4">
          <div className="bg-white rounded-lg p-4">
            <div className="flex items-start gap-3 mb-3">
              <ChefHat className="w-5 h-5 text-purple-600 flex-shrink-0 mt-0.5" />
              <div className="flex-1">
                <h3 className="font-bold text-gray-900 mb-1">
                  {topSuggestion.suggestion}
                </h3>
                <p className="text-sm text-gray-600 mb-2">
                  {topSuggestion.recipe}
                </p>
                <div className="flex items-center gap-2 text-xs">
                  <span className="bg-purple-100 text-purple-700 px-2 py-1 rounded-full font-medium">
                    {topSuggestion.cuisine}
                  </span>
                  <span className="bg-green-100 text-green-700 px-2 py-1 rounded-full font-medium">
                    {topSuggestion.meals} meals
                  </span>
                  <span className="bg-blue-100 text-blue-700 px-2 py-1 rounded-full font-medium flex items-center gap-1">
                    <TrendingUp className="w-3 h-3" />
                    {topSuggestion.confidence}% match
                  </span>
                </div>
              </div>
            </div>

            <div className="border-t pt-3 mt-3">
              <p className="text-xs font-semibold text-gray-700 mb-2">You have:</p>
              <div className="flex flex-wrap gap-1 mb-3">
                {topSuggestion.have.map((item: string, idx: number) => (
                  <span key={idx} className="text-xs bg-green-50 text-green-700 px-2 py-1 rounded">
                    ✓ {item}
                  </span>
                ))}
              </div>
              <p className="text-xs font-semibold text-gray-700 mb-2">Missing:</p>
              <p className="text-sm text-orange-600 font-medium">
                {topSuggestion.missing}
              </p>
            </div>
          </div>

          {suggestions.length > 1 && (
            <div className="space-y-2">
              <p className="text-xs font-semibold text-gray-600">More suggestions:</p>
              {suggestions.slice(1, 3).map((sug: any) => (
                <div key={sug.id} className="bg-white rounded-lg p-3">
                  <p className="font-medium text-sm text-gray-900">{sug.suggestion}</p>
                  <p className="text-xs text-gray-600 mt-1">Missing: {sug.missing}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      ) : (
        <div className="text-center py-8">
          <Lightbulb className="w-12 h-12 text-gray-300 mx-auto mb-3" />
          <p className="text-gray-500 text-sm">No suggestions available</p>
        </div>
      )}
    </div>
  )
}
