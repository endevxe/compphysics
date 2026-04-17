import { supabase } from './supabase.js'

// ── Element refs ────────────────────────────────────────────────
const modal       = document.getElementById('auth-modal')
const backdrop    = document.getElementById('auth-backdrop')
const authTitle   = document.getElementById('auth-title')
const emailInput  = document.getElementById('auth-email')
const passInput   = document.getElementById('auth-password')
const errorMsg    = document.getElementById('auth-error')
const submitBtn   = document.getElementById('btn-submit')
const toggleLink  = document.getElementById('auth-toggle')
const switchText  = document.getElementById('auth-switch')
const openBtn     = document.getElementById('btn-open-auth')
const signoutBtn  = document.getElementById('btn-signout')
const emailDisplay= document.getElementById('user-email-display')

let isSignUp = false  // toggles between sign in / sign up mode

// ── Open / close modal ───────────────────────────────────────────
openBtn.addEventListener('click', () => showModal())
document.getElementById('auth-close').addEventListener('click', hideModal)
backdrop.addEventListener('click', hideModal)

function showModal() {
  modal.style.display = 'block'
  emailInput.focus()
}
function hideModal() {
  modal.style.display = 'none'
  errorMsg.textContent = ''
  emailInput.value = ''
  passInput.value  = ''
}

// ── Toggle between Sign in ↔ Sign up ────────────────────────────
toggleLink.addEventListener('click', (e) => {
  e.preventDefault()
  isSignUp = !isSignUp
  authTitle.textContent  = isSignUp ? 'Create account' : 'Sign in'
  submitBtn.textContent  = isSignUp ? 'Sign up'        : 'Sign in'
  switchText.innerHTML   = isSignUp
    ? `Already have an account? <a id="auth-toggle" href="#">Sign in</a>`
    : `Don't have an account? <a id="auth-toggle" href="#">Sign up</a>`
  // Re-attach listener after innerHTML swap
  document.getElementById('auth-toggle').addEventListener('click', toggleLink.onclick)
  errorMsg.textContent = ''
})

// ── Google OAuth ─────────────────────────────────────────────────
document.getElementById('btn-google').addEventListener('click', async () => {
  const { error } = await supabase.auth.signInWithOAuth({
    provider: 'google',
    options: { redirectTo: window.location.origin }
  })
  if (error) errorMsg.textContent = error.message
})

// ── Email submit (sign in OR sign up) ────────────────────────────
submitBtn.addEventListener('click', async () => {
  const email    = emailInput.value.trim()
  const password = passInput.value
  errorMsg.textContent  = ''
  submitBtn.disabled    = true
  submitBtn.textContent = 'Please wait...'

  let error

  if (isSignUp) {
    ;({ error } = await supabase.auth.signUp({ email, password }))
    if (!error) {
      errorMsg.style.color = 'green'
      errorMsg.textContent = 'Check your email to confirm your account!'
    }
  } else {
    ;({ error } = await supabase.auth.signInWithPassword({ email, password }))
  }

  if (error) {
    errorMsg.style.color  = '#dc2626'
    errorMsg.textContent  = error.message
  }

  submitBtn.disabled    = false
  submitBtn.textContent = isSignUp ? 'Sign up' : 'Sign in'
})

// ── Sign out ─────────────────────────────────────────────────────
signoutBtn.addEventListener('click', async () => {
  await supabase.auth.signOut()
})

// ── Auth state listener ──────────────────────────────────────────
// This is the single source of truth for UI state
supabase.auth.onAuthStateChange((event, session) => {
  if (event === 'SIGNED_IN') {
    hideModal()
    openBtn.style.display        = 'none'
    signoutBtn.style.display     = 'inline-block'
    emailDisplay.style.display   = 'inline'
    emailDisplay.textContent     = session.user.email
  }
  if (event === 'SIGNED_OUT') {
    openBtn.style.display        = 'inline-block'
    signoutBtn.style.display     = 'none'
    emailDisplay.style.display   = 'none'
    emailDisplay.textContent     = ''
  }
})
