import 'react-native-url-polyfill/auto';
import {createClient} from '@supabase/supabase-js';
const supabaseUrl = 'https://wedprccshkryxfzhjyvl.supabase.co';
const supabaseKey =
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndlZHByY2NzaGtyeXhmemhqeXZsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcxNzk0MDksImV4cCI6MjA3Mjc1NTQwOX0.jvyWP-sYoUiJqNyG73Zczu_cSbOdUnJXtAdZ1Wsbk-g';
export const supabase = createClient(supabaseUrl, supabaseKey);
