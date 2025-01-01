from pymongo import MongoClient
import time
import pandas as pd
import matplotlib.pyplot as plt

def calculate_statistics(db):
    stats = []
    while True:
        start_time = time.time()
        files_count = db['files'].count_documents({})
        chunks_count = db['chunks'].count_documents({})
        candidates_count = db['candidates'].count_documents({})
        clones_count = db['clones'].count_documents({})
        elapsed_time = time.time() - start_time
        
        stats.append({
            'timestamp': time.time(),
            'files': files_count,
            'chunks': chunks_count,
            'candidates': candidates_count,
            'clones': clones_count,
            'elapsed_time': elapsed_time
        })
        
        if len(stats) > 1:
            df = pd.DataFrame(stats)
            df['time_per_chunk'] = df['elapsed_time'] / df['chunks'].diff().fillna(0)
            print(df.tail())
        
        time.sleep(10)

def plot_statistics(df):
    plt.figure(figsize=(10, 6))
    plt.plot(df['timestamp'], df['time_per_chunk'], label='Time per Chunk')
    plt.xlabel('Time')
    plt.ylabel('Processing Time (s)')
    plt.legend()
    plt.show()

def monitor_database():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['cloneDetector']
    
    # Start calculating statistics
    calculate_statistics(db)
    
    # Optionally, plot statistics
    stats = list(db['statistics'].find().sort("timestamp", 1))
    df = pd.DataFrame(stats)
    plot_statistics(df)

if __name__ == "__main__":
    monitor_database()