// Thin wrapper around the Python bridge that pywebview injects as
// `window.pywebview.api`. The bridge isn't available until the
// `pywebviewready` event fires, so every call waits for that first.
export interface SignupSlot {
  id: number
  name: string
  slots_total: number
  slots_filled: number
}

export interface SignupEvent {
  id: number
  title: string
  url: string
  slots: SignupSlot[]
  last_synced: string | null
}

interface PywebviewApi {
  ping(): Promise<string>
  list_events(): Promise<SignupEvent[]>
  refresh_events(): Promise<SignupEvent[]>
}

declare global {
  interface Window {
    pywebview?: { api: PywebviewApi }
  }
}

let readyPromise: Promise<void> | null = null

function waitForBridge(): Promise<void> {
  if (window.pywebview) return Promise.resolve()

  readyPromise ??= new Promise((resolve) => {
    window.addEventListener('pywebviewready', () => resolve(), { once: true })
  })

  return readyPromise
}

export async function getApi(): Promise<PywebviewApi> {
  await waitForBridge()
  if (!window.pywebview) {
    throw new Error('pywebview bridge unavailable (running outside the desktop shell?)')
  }
  return window.pywebview.api
}
