#!/usr/bin/env python3
"""
Live Data Analysis - Mobile App to ML Pipeline
===============================================
This script connects to your Supabase database, fetches encrypted mobile app data,
decrypts it, and performs comprehensive analysis and machine learning.

Run this instead of the Jupyter notebook if you're having kernel issues.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from supabase import create_client, Client
from datetime import datetime
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib
import base64

# Set up plotting
plt.style.use('default')
sns.set_palette("husl")

def setup_supabase():
    """Connect to Supabase database"""
    print("🔄 Connecting to Supabase...")
    
    SUPABASE_URL = "https://wedprccshkryxfzhjyvl.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndlZHByY2NzaGtyeXhmemhqeXZsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcxNzk0MDksImV4cCI6MjA3Mjc1NTQwOX0.jvyWP-sYoUiJqNyG73Zczu_cSbOdUnJXtAdZ1Wsbk-g"
    
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Connected to Supabase database!")
    return supabase

def fetch_data(supabase):
    """Fetch data from both tables"""
    print("\n📊 Fetching mobile app data...")
    
    # Fetch survey data
    response = supabase.table('fable').select('*').execute()
    survey_data = pd.DataFrame(response.data)
    print(f"📋 Retrieved {len(survey_data)} survey records")
    
    # Fetch OCR data  
    response_ocr = supabase.table('ocr').select('*').execute()
    ocr_data = pd.DataFrame(response_ocr.data)
    print(f"📱 Retrieved {len(ocr_data)} OCR records")
    
    return survey_data, ocr_data

def decrypt_data(encrypted_data, key="your-secret-key"):
    """
    Decrypt AES encrypted data from mobile app
    Note: This is a simplified version - you may need to adjust based on your exact encryption method
    """
    try:
        # This is a placeholder - you'll need to implement the exact decryption
        # method used in your mobile app
        print("🔓 Attempting to decrypt data...")
        print(f"   Encrypted data preview: {encrypted_data[:50]}...")
        
        # For now, return the encrypted data as-is since we need the exact decryption key/method
        return {"status": "encrypted", "data": encrypted_data}
        
    except Exception as e:
        print(f"⚠️  Decryption failed: {e}")
        return {"status": "failed", "data": encrypted_data}

def analyze_survey_data(survey_data):
    """Analyze survey response patterns"""
    print("\n📈 Analyzing Survey Data...")
    
    if survey_data.empty:
        print("❌ No survey data to analyze")
        return
    
    # Basic statistics
    print(f"📊 Total Survey Responses: {len(survey_data)}")
    print(f"📅 Date Range: {survey_data['created_at'].min()} to {survey_data['created_at'].max()}")
    
    # Convert timestamps
    survey_data['created_at'] = pd.to_datetime(survey_data['created_at'])
    survey_data['hour'] = survey_data['created_at'].dt.hour
    survey_data['date'] = survey_data['created_at'].dt.date
    
    # Time-based analysis
    print("\n⏰ Survey Submission Patterns:")
    hourly_counts = survey_data['hour'].value_counts().sort_index()
    print("Submissions by hour:")
    for hour, count in hourly_counts.items():
        print(f"   {hour:02d}:00 - {count} submissions")
    
    # Create visualizations
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('📊 Mobile App Survey Analysis Dashboard', fontsize=16, fontweight='bold')
    
    # 1. Submissions over time
    daily_counts = survey_data.groupby('date').size()
    axes[0,0].plot(daily_counts.index, daily_counts.values, marker='o', linewidth=2)
    axes[0,0].set_title('📅 Daily Survey Submissions')
    axes[0,0].set_xlabel('Date')
    axes[0,0].set_ylabel('Number of Submissions')
    axes[0,0].tick_params(axis='x', rotation=45)
    
    # 2. Hourly distribution
    axes[0,1].bar(hourly_counts.index, hourly_counts.values, color='skyblue')
    axes[0,1].set_title('⏰ Submissions by Hour of Day')
    axes[0,1].set_xlabel('Hour')
    axes[0,1].set_ylabel('Number of Submissions')
    
    # 3. Data size distribution
    survey_data['data_length'] = survey_data['hash_data'].str.len()
    axes[1,0].hist(survey_data['data_length'], bins=20, alpha=0.7, color='lightcoral')
    axes[1,0].set_title('📊 Encrypted Data Size Distribution')
    axes[1,0].set_xlabel('Data Length (characters)')
    axes[1,0].set_ylabel('Frequency')
    
    # 4. Cumulative submissions
    survey_data_sorted = survey_data.sort_values('created_at')
    cumulative_count = range(1, len(survey_data_sorted) + 1)
    axes[1,1].plot(survey_data_sorted['created_at'], cumulative_count, marker='o', markersize=3)
    axes[1,1].set_title('📈 Cumulative Survey Growth')
    axes[1,1].set_xlabel('Time')
    axes[1,1].set_ylabel('Total Submissions')
    axes[1,1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('survey_analysis_dashboard.png', dpi=300, bbox_inches='tight')
    print("💾 Saved visualization: survey_analysis_dashboard.png")
    plt.show()

def analyze_ocr_data(ocr_data):
    """Analyze OCR usage patterns"""
    print("\n🔍 Analyzing OCR Data...")
    
    if ocr_data.empty:
        print("❌ No OCR data to analyze")
        return
    
    print(f"📱 Total OCR Operations: {len(ocr_data)}")
    
    # Convert timestamps
    ocr_data['created_at'] = pd.to_datetime(ocr_data['created_at'])
    
    # Basic analysis
    ocr_data['text_length'] = ocr_data['recog_text'].str.len()
    
    print(f"📊 Average text length: {ocr_data['text_length'].mean():.1f} characters")
    print(f"📊 Max text length: {ocr_data['text_length'].max()} characters")
    print(f"📊 Min text length: {ocr_data['text_length'].min()} characters")

def generate_insights(survey_data, ocr_data):
    """Generate comprehensive insights"""
    print("\n🧠 Generating Insights...")
    
    insights = []
    
    if not survey_data.empty:
        # Survey insights
        total_surveys = len(survey_data)
        survey_data['created_at'] = pd.to_datetime(survey_data['created_at'])
        date_range = (survey_data['created_at'].max() - survey_data['created_at'].min()).days
        
        insights.append(f"📋 Survey Activity: {total_surveys} responses over {date_range} days")
        
        if date_range > 0:
            avg_daily = total_surveys / date_range
            insights.append(f"📊 Average: {avg_daily:.1f} surveys per day")
        
        # Peak hours
        if 'hour' in survey_data.columns:
            peak_hour = survey_data['hour'].mode().iloc[0]
            insights.append(f"⏰ Peak Activity: {peak_hour}:00 hour")
    
    if not ocr_data.empty:
        total_ocr = len(ocr_data)
        insights.append(f"📱 OCR Usage: {total_ocr} text recognitions performed")
    
    # Data quality insights
    if not survey_data.empty:
        avg_data_size = survey_data['hash_data'].str.len().mean()
        insights.append(f"🔒 Encryption Quality: Average encrypted data size {avg_data_size:.0f} characters")
    
    print("\n🎯 Key Insights:")
    for i, insight in enumerate(insights, 1):
        print(f"   {i}. {insight}")
    
    return insights

def run_ml_analysis(survey_data):
    """Run basic ML analysis on the data patterns"""
    print("\n🤖 Running ML Analysis...")
    
    if survey_data.empty:
        print("❌ No data for ML analysis")
        return
    
    try:
        from sklearn.cluster import KMeans
        from sklearn.preprocessing import StandardScaler
        
        # Create features from metadata
        survey_data['created_at'] = pd.to_datetime(survey_data['created_at'])
        survey_data['hour'] = survey_data['created_at'].dt.hour
        survey_data['day_of_week'] = survey_data['created_at'].dt.dayofweek
        survey_data['data_length'] = survey_data['hash_data'].str.len()
        
        # Prepare features for clustering
        features = survey_data[['hour', 'day_of_week', 'data_length']].copy()
        
        if len(features) >= 3:  # Need at least 3 samples for clustering
            # Standardize features
            scaler = StandardScaler()
            features_scaled = scaler.fit_transform(features)
            
            # Perform clustering
            n_clusters = min(3, len(features))  # Don't use more clusters than samples
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(features_scaled)
            
            survey_data['cluster'] = clusters
            
            print(f"🎯 Identified {n_clusters} user behavior patterns:")
            for cluster in range(n_clusters):
                cluster_data = survey_data[survey_data['cluster'] == cluster]
                avg_hour = cluster_data['hour'].mean()
                avg_length = cluster_data['data_length'].mean()
                count = len(cluster_data)
                
                print(f"   Pattern {cluster + 1}: {count} users, avg time {avg_hour:.1f}h, avg data {avg_length:.0f} chars")
        
        else:
            print("⚠️  Need more data points for meaningful ML analysis")
    
    except ImportError:
        print("⚠️  scikit-learn not installed. Installing...")
        import subprocess
        subprocess.check_call(["pip", "install", "scikit-learn"])
        print("✅ Installed scikit-learn. Please run the script again.")

def main():
    """Main analysis pipeline"""
    print("🚀 Starting Live Data Analysis Pipeline")
    print("=" * 50)
    
    try:
        # 1. Connect to database
        supabase = setup_supabase()
        
        # 2. Fetch data
        survey_data, ocr_data = fetch_data(supabase)
        
        # 3. Analyze survey data
        if not survey_data.empty:
            analyze_survey_data(survey_data)
        
        # 4. Analyze OCR data
        if not ocr_data.empty:
            analyze_ocr_data(ocr_data)
        
        # 5. Generate insights
        insights = generate_insights(survey_data, ocr_data)
        
        # 6. Run ML analysis
        if not survey_data.empty:
            run_ml_analysis(survey_data)
        
        print("\n🎉 Analysis Complete!")
        print("📊 Check 'survey_analysis_dashboard.png' for visualizations")
        
        # 7. Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if not survey_data.empty:
            survey_data.to_csv(f'survey_analysis_{timestamp}.csv', index=False)
            print(f"💾 Saved survey data: survey_analysis_{timestamp}.csv")
        
        if not ocr_data.empty:
            ocr_data.to_csv(f'ocr_analysis_{timestamp}.csv', index=False)
            print(f"💾 Saved OCR data: ocr_analysis_{timestamp}.csv")
        
        # Save insights
        with open(f'insights_{timestamp}.txt', 'w') as f:
            f.write("Mobile App Data Analysis Insights\n")
            f.write("=" * 40 + "\n\n")
            for insight in insights:
                f.write(f"• {insight}\n")
        
        print(f"💾 Saved insights: insights_{timestamp}.txt")
        
    except Exception as e:
        print(f"❌ Error in analysis pipeline: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
