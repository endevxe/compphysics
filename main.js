import { supabase } from './supabase.js'

// ── Test: check if Supabase connection works ──────────────────────
async function testConnection() {
  const { data, error } = await supabase.auth.getSession()

  if (error) {
    console.error('Supabase error:', error.message)
    return
  }

  // data.session will be null if no user is logged in — that's fine
  console.log('Supabase connected. Session:', data.session ?? 'No active session')
}

testConnection()

// ── Auth state listener (add this once at the top level) ─────────
// Fires whenever the user logs in, logs out, or their token refreshes
supabase.auth.onAuthStateChange((event, session) => {
  console.log('Auth event:', event, session?.user?.email)

  if (event === 'SIGNED_IN')  handleSignIn(session.user)
  if (event === 'SIGNED_OUT') handleSignOut()
})

function handleSignIn(user) {
  // TODO in Phase 2: show dashboard, hide login UI
  console.log('User signed in:', user.email)
}

function handleSignOut() {
  // TODO in Phase 2: show login UI, clear user state
  console.log('User signed out')
}
