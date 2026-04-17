// supabase.js — import this wherever you need DB or auth access
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const SUPABASE_URL  = 'https://xyuhqxkonlcmgejhqqef.supabase.co'
const SUPABASE_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh5dWhxeGtvbmxjbWdlamhxcWVmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYzOTQzNDIsImV4cCI6MjA5MTk3MDM0Mn0.scZ3UdFt1n4XP0rUBWyXiyMbsOavfQnPJqEwWASqE2A'

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON)
