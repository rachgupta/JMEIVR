import argparse
from pathlib import Path
from add_song import add_song
from database import init_database, load_database
from song_recognize import test_sample

# Set up parameters
parser = argparse.ArgumentParser(description="Automatically recognize songs")
parser.add_argument("--update", "-u", action="store_true", help="Update the song database")
parser.add_argument("--list", "-l", type=Path, help="View list of files")
parser.add_argument("--init", "-i", type=Path, help="Initialize the database")
parser.add_argument("--add", "-a", type=Path, help="Path to MP3 file to add")
parser.add_argument("--title", "-t", help="Song title to add")
parser.add_argument("--artist", "-A", help="Song artist to add")
parser.add_argument("--year", "-y", help="Song year to add")
parser.add_argument("--database", "-d", type=Path, help="Use alternate database path when recognizing")

# Get args
args = parser.parse_args()

if args.update:
	# Update the database
	add_song(args.title, args.artist, args.year, args.add, args.database)
elif args.list != None:
	# List the database
	metadata, fingerprint_database = load_database(args.list)

	for name, artist, year in metadata:
		print(f"{name} by {artist} ({year})")
elif args.init != None:
	# Initialize the database
	init_database(args.init)
else:
	# Recognize the song
	load_database(args.database)
	song_id, offset, past_cutoff = test_sample(10)

	if not past_cutoff:
		print("Song not in database, closest match:")

	metadata, fingerprint_database = load_database(args.database)
	name, artist, year, time = metadata[song_id]
	print(f"{name} by {artist} ({year})")