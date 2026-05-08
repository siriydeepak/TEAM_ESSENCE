import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'
import { Cloud, Droplets, AlertTriangle, MapPin } from 'lucide-react'
import toast from 'react-hot-toast'

export default function WeatherImpact() {
  const [city, setCity] = useState('')
  const [showInput, setShowInput] = useState(false)
  const queryClient = useQueryClient()

  const { data: weather, isLoading } = useQuery({
    queryKey: ['weather'],
    queryFn: async () => {
      const res = await axios.get('/api/weather/shelf-impact')
      return res.data
    },
    refetchInterval: 300000, // Refresh every 5 minutes
  })

  const updateLocationMutation = useMutation({
    mutationFn: async (cityName: string) => {
      const res = await axios.post('/api/weather/location', { city: cityName })
      return res.data
    },
    onSuccess: (data) => {
      toast.success(`Location updated to ${data.city}`)
      queryClient.invalidateQueries({ queryKey: ['weather'] })
      queryClient.invalidateQueries({ queryKey: ['inventory'] })
      setShowInput(false)
      setCity('')
    },
    onError: () => {
      toast.error('Failed to update location')
    },
  })

  const handleUpdateLocation = (e: React.FormEvent) => {
    e.preventDefault()
    if (city.trim()) {
      updateLocationMutation.mutate(city)
    }
  }

  if (isLoading) {
    return (
      <div className="bg-white rounded-xl shadow-sm p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="h-20 bg-gray-200 rounded"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-xl shadow-sm p-6 border border-blue-100">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <Cloud className="w-6 h-6 text-blue-600" />
          <h2 className="text-xl font-bold text-gray-900">Weather Impact</h2>
        </div>
        <button
          onClick={() => setShowInput(!showInput)}
          className="flex items-center gap-2 px-3 py-1.5 bg-white rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition"
        >
          <MapPin className="w-4 h-4" />
          Change Location
        </button>
      </div>

      {showInput && (
        <form onSubmit={handleUpdateLocation} className="mb-4">
          <div className="flex gap-2">
            <input
              type="text"
              value={city}
              onChange={(e) => setCity(e.target.value)}
              placeholder="Enter city name"
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none"
            />
            <button
              type="submit"
              disabled={updateLocationMutation.isPending}
              className="px-4 py-2 bg-primary text-white rounded-lg font-medium hover:bg-primary/90 transition disabled:opacity-50"
            >
              {updateLocationMutation.isPending ? 'Updating...' : 'Update'}
            </button>
          </div>
        </form>
      )}

      {weather && (
        <div className="space-y-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white rounded-lg p-4">
              <div className="flex items-center gap-2 text-gray-600 mb-1">
                <Cloud className="w-4 h-4" />
                <span className="text-sm">Temperature</span>
              </div>
              <p className="text-2xl font-bold text-gray-900">
                {weather.temperature_celsius}°C
              </p>
            </div>

            <div className="bg-white rounded-lg p-4">
              <div className="flex items-center gap-2 text-gray-600 mb-1">
                <Droplets className="w-4 h-4" />
                <span className="text-sm">Humidity</span>
              </div>
              <p className="text-2xl font-bold text-gray-900">
                {weather.humidity}%
              </p>
            </div>

            <div className="bg-white rounded-lg p-4">
              <div className="flex items-center gap-2 text-gray-600 mb-1">
                <AlertTriangle className="w-4 h-4" />
                <span className="text-sm">Shelf Impact</span>
              </div>
              <p className="text-2xl font-bold text-orange-600">
                -{weather.flux_penalty_pct}%
              </p>
            </div>

            <div className="bg-white rounded-lg p-4">
              <div className="flex items-center gap-2 text-gray-600 mb-1">
                <span className="text-sm">Status</span>
              </div>
              <p className={`text-sm font-bold ${weather.alert ? 'text-red-600' : 'text-green-600'}`}>
                {weather.alert ? 'High Risk' : 'Normal'}
              </p>
            </div>
          </div>

          {weather.alert && (
            <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
              <div className="flex items-start gap-3">
                <AlertTriangle className="w-5 h-5 text-orange-600 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="font-semibold text-orange-900 mb-1">Weather Alert</p>
                  <p className="text-sm text-orange-800">
                    {weather.message || 'High temperature and humidity detected. Perishable items may spoil faster.'}
                  </p>
                  {weather.adjustments && weather.adjustments.length > 0 && (
                    <div className="mt-3 space-y-1">
                      <p className="text-xs font-semibold text-orange-900">Affected Items:</p>
                      {weather.adjustments.map((adj: any, idx: number) => (
                        <p key={idx} className="text-xs text-orange-800">
                          • {adj.item}: {adj.original_days}d → {adj.adjusted_days}d
                        </p>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
