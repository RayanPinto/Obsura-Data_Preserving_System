#!/usr/bin/env python3
"""
Simple Data Viewer - See Your Mobile App Data
=============================================
This script shows you EXACTLY what data you submitted through your mobile app
in a simple, easy-to-understand format.
"""

from supabase import create_client, Client
import json
from datetime import datetime

def connect_to_database():
    """Connect to your Supabase database"""
    print("🔄 Connecting to your database...")
    
    SUPABASE_URL = "https://wedprccshkryxfzhjyvl.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndlZHByY2NzaGtyeXhmemhqeXZsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcxNzk0MDksImV4cCI6MjA3Mjc1NTQwOX0.jvyWP-sYoUiJqNyG73Zczu_cSbOdUnJXtAdZ1Wsbk-g"
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Connected successfully!")
    return supabase

def show_your_survey_data(supabase):
    """Show all the survey data you submitted through the mobile app"""
    print("\n" + "="*60)
    print("📋 YOUR SURVEY SUBMISSIONS")
    print("="*60)
    
    # Get your survey data
    response = supabase.table('fable').select('*').execute()
    surveys = response.data
    
    if not surveys:
        print("❌ No survey data found. Please submit a survey through your mobile app first.")
        return
    
    print(f"📊 Total surveys you submitted: {len(surveys)}")
    print()
    
    # Show each survey submission
    for i, survey in enumerate(surveys, 1):
        print(f"📝 Survey #{i}")
        print(f"   📅 Submitted on: {survey['created_at']}")
        print(f"   🆔 Record ID: {survey['id']}")
        print(f"   🔒 Your encrypted data: {survey['hash_data'][:100]}...")
        print(f"      (This is your survey answers, encrypted for privacy)")
        print()
    
    # Show timing information
    if len(surveys) > 1:
        first_survey = min(surveys, key=lambda x: x['created_at'])
        last_survey = max(surveys, key=lambda x: x['created_at'])
        
        print("⏰ TIMING INFORMATION:")
        print(f"   First survey: {first_survey['created_at']}")
        print(f"   Latest survey: {last_survey['created_at']}")
        print()

def show_your_ocr_data(supabase):
    """Show all the OCR (text recognition) data from your mobile app"""
    print("\n" + "="*60)
    print("📱 YOUR OCR (TEXT RECOGNITION) DATA")
    print("="*60)
    
    # Get your OCR data
    response = supabase.table('ocr').select('*').execute()
    ocr_records = response.data
    
    if not ocr_records:
        print("❌ No OCR data found. You haven't used the text recognition feature yet.")
        print("💡 Try taking a photo of text in your mobile app's OCR tab!")
        return
    
    print(f"📸 Total text recognitions: {len(ocr_records)}")
    print()
    
    # Show each OCR result
    for i, ocr in enumerate(ocr_records, 1):
        print(f"📸 OCR #{i}")
        print(f"   📅 Processed on: {ocr['created_at']}")
        print(f"   🆔 Record ID: {ocr['id']}")
        print(f"   🔒 Recognized text (encrypted): {ocr['recog_text'][:100]}...")
        print(f"      (This is the text from your photo, encrypted for privacy)")
        print()

def explain_what_happens():
    """Explain what happens to your data"""
    print("\n" + "="*60)
    print("🤔 WHAT HAPPENS TO YOUR DATA?")
    print("="*60)
    
    print("1. 📱 You fill out surveys or take photos in your mobile app")
    print("2. 🔒 Your data gets ENCRYPTED (scrambled) for privacy")
    print("3. 📤 The encrypted data is sent to your secure database")
    print("4. 💾 It's stored safely in your Supabase database")
    print("5. 📊 You can view it here (still encrypted)")
    print("6. 🧪 Later, it can be used for research/analysis")
    print()
    print("🛡️  PRIVACY: Your actual answers are never stored in plain text!")
    print("🔐 Only you have the encryption key to read the real content.")
    print()

def show_simple_summary(supabase):
    """Show a simple summary of your app usage"""
    print("\n" + "="*60)
    print("📈 SIMPLE SUMMARY")
    print("="*60)
    
    # Count surveys
    surveys = supabase.table('fable').select('*').execute().data
    ocr_records = supabase.table('ocr').select('*').execute().data
    
    print(f"📋 Survey submissions: {len(surveys)}")
    print(f"📱 OCR text recognitions: {len(ocr_records)}")
    print(f"📊 Total app interactions: {len(surveys) + len(ocr_records)}")
    print()
    
    if surveys:
        # Show when you're most active
        from collections import Counter
        
        # Extract hours from timestamps
        hours = []
        for survey in surveys:
            timestamp = survey['created_at']
            # Extract hour from timestamp (simple approach)
            if 'T' in timestamp and ':' in timestamp:
                time_part = timestamp.split('T')[1]
                hour = int(time_part.split(':')[0])
                hours.append(hour)
        
        if hours:
            hour_counts = Counter(hours)
            most_active_hour = max(hour_counts, key=hour_counts.get)
            print(f"⏰ You're most active at: {most_active_hour}:00")
            print(f"📅 You used the app on {len(set(s['created_at'][:10] for s in surveys))} different days")
    
    print()
    print("💡 The more you use the app, the more data you'll have for analysis!")

def main():
    """Main function - show your data in a simple way"""
    print("🚀 SIMPLE DATA VIEWER")
    print("See exactly what data you submitted through your mobile app")
    print()
    
    try:
        # Connect to database
        supabase = connect_to_database()
        
        # Show your survey data
        show_your_survey_data(supabase)
        
        # Show your OCR data
        show_your_ocr_data(supabase)
        
        # Show simple summary
        show_simple_summary(supabase)
        
        # Explain what happens to data
        explain_what_happens()
        
        print("✅ That's it! This is all the data from your mobile app.")
        print("🔄 Run this script again after using your app more to see new data!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you're connected to the internet and try again.")

if __name__ == "__main__":
    main()
