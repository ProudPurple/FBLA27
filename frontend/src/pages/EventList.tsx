import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getApi, type SignupEvent } from '../lib/pywebview'

function EventList() {
  const [events, setEvents] = useState<SignupEvent[]>([])
  const [status, setStatus] = useState<'loading' | 'ready' | 'error'>('loading')
  const [refreshing, setRefreshing] = useState(false)

  useEffect(() => {
    getApi()
      .then((api) => api.list_events())
      .then((data) => {
        setEvents(data)
        setStatus('ready')
      })
      .catch((err) => {
        console.error(err)
        setStatus('error')
      })
  }, [])

  async function handleRefresh() {
    setRefreshing(true)
    try {
      const api = await getApi()
      setEvents(await api.refresh_events())
    } catch (err) {
      console.error(err)
      setStatus('error')
    } finally {
      setRefreshing(false)
    }
  }

  
  return (
    <div>
      <header className="mb-8 flex items-center justify-between">
        <h1 className="text-3xl font-semibold">Event List</h1>
        <button
          type="button"
          onClick={handleRefresh}
          disabled={refreshing || status === 'loading'}
          className="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {refreshing ? 'Refreshing…' : 'Refresh'}
        </button>
      </header>

      {status === 'error' && (
        <p className="rounded-md bg-red-50 px-4 py-3 text-sm text-red-700">
          Couldn't reach the Python backend. If you're viewing this in a regular
          browser (not the desktop app), the pywebview bridge isn't available.
        </p>
      )}

      {status === 'loading' && <p className="text-sm text-slate-500">Loading events…</p>}

      {status === 'ready' && events.length === 0 && (
        <p className="text-sm text-slate-500">No events yet. Hit refresh to scrape SignUpGenius.</p>
      )}

      <ul className="divide-y divide-slate-200 rounded-lg border border-slate-200">
        {events.map((event) => (
          <li key={event.id} className="flex items-center justify-between px-4 py-3">
            <div>
              <Link to={`/event/${event.id}`} state={event}>
                {event.title}
              </Link>
              <p className="text-xs text-slate-500">
                {event.last_synced ? `Synced ${event.last_synced}` : 'Never synced'}
              </p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default EventList
