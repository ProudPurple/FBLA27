import { Link, useLocation } from 'react-router-dom'
import type { SignupEvent } from '../lib/pywebview'

function Event() {
    const location = useLocation()
    const event = location.state as SignupEvent

    return (
        <div>
            <header className="mb-8 flex items-center justify-between">
                <h1 className="text-3xl font-semibold">{event?.title}</h1>
                <Link to="/">
                    <button
                        type="button"
                        className="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        Back to Event List
                    </button>
                </Link>
            </header>
            <div className="border-t border-slate-200 pt-6">
                <h2 className="mb-4 text-2xl font-medium">Participants</h2>
                <p>
                    {event.slots.map((slot) => (
                        <div key={slot.id} className="mb-4 rounded-md border border-slate-200 p-4">
                            <p className="text-xl font-medium">{slot.name}</p>
                            <p className="text-md text-slate-500">
                                {slot.slots_filled}/{slot.slots_total} slots filled
                            </p>
                        </div>
                    ))}
                </p>
            </div>
        </div>
    )
}

export default Event