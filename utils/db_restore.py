import os
import boto3
import psycopg2
import time
import subprocess
from pathlib import Path
import logging
logger = logging.getLogger(__name__)

class DbRestore:
    def __init__(self):
        self.conn = None
        self.s3_bucket = os.getenv("S3_BUCKET_NAME")  # Name of the S3 bucket
        self.s3_backup_key = os.getenv("S3_BACKUP_KEY")  # Object key (file path in S3)
        self.local_backup_path = (
            "./tmp/db_backup.dump"  # Local path to store downloaded backup
        )

    def connect(self, super: bool = False):
        self.conn = self.create_connection(super=super)  # Connect as superuser to 'postgres'
        self.conn.autocommit = True

    def create_connection(self, super: bool = False):
        return psycopg2.connect(
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT"),
            user=os.getenv("PG_SUPERUSER") if super else os.getenv("PG_USER"),
            password=os.getenv("PG_SUPERPASS") if super else os.getenv("PG_PASS"),
            dbname="postgres" if super else os.getenv("PG_DBNAME"),
        )

    def recreate_db(self):
        db_name = os.getenv("PG_DBNAME")
        self.connect(super=True)  # Connect as superuser to 'postgres'
        with self.conn.cursor() as cur:
            cur.execute(f'ALTER DATABASE "{db_name}" OWNER TO {os.getenv("PG_SUPERUSER")};')
            logging.info(f"Dropping and recreating database: {db_name}")
            cur.execute(f'DROP DATABASE IF EXISTS "{db_name}"')
            cur.execute(f'CREATE DATABASE "{db_name}"')
            cur.execute('CREATE SCHEMA IF NOT EXISTS bss')
            cur.execute(f'ALTER DATABASE "{db_name}" OWNER TO {os.getenv("PG_USER")};')
            logging.info(f"Database {db_name} recreated successfully.")

    def disconnect(self):
        """Close the database connection."""
        if self.conn:
            try:
                self.conn.close()
            except Exception as e:
                logging.info(f"NO connection found to disconnect from! - {e}")

    def download_backup_from_s3(self, profile_name: str):
        """Download the database backup from S3 to a local temporary file."""

        try:
            logging.info(f"Downloading backup from S3 bucket: {self.s3_bucket}, key: {self.s3_backup_key} with profile: {profile_name}")
            session = boto3.Session(profile_name=profile_name)
            s3 = session.client("s3")
            Path(os.path.dirname(self.local_backup_path)).mkdir(parents=True, exist_ok=True)
            s3.download_file(self.s3_bucket, self.s3_backup_key, self.local_backup_path)
            logging.info("Backup downloaded successfully.")
        except Exception as e:
            raise

    def restore_backup(self):
        """Restore the database from the downloaded backup."""
        logging.info("Restoring database from backup...")
        os.environ["PGPASSWORD"] = os.getenv("PG_PASS")
        subprocess.run(
            [
                "psql", # for text dump file psql is used, for binary dump file pg_restore is used
                "-q",
                # "--clean",
                "-h",
                os.getenv("PG_HOST"),
                "-p",
                os.getenv("PG_PORT"),
                "-U",
                os.getenv("PG_USER"),
                "-d",
                os.getenv("PG_DBNAME"),
                # "-j",
                # os.getenv("J_VALUE"),
                "-f",
                self.local_backup_path,
            ],
            check=False,
        )

    def kill_all_db_sessions(self):
        """Terminate all active sessions for the target database."""
        dbname = os.getenv("PG_DBNAME")
        # Always connect to 'postgres' or another database, NOT the target db
        self.disconnect()
        self.connect(super=True)
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT pg_terminate_backend(pg_stat_activity.pid)
                    FROM pg_stat_activity
                    WHERE datname = '{dbname}' AND pid <> pg_backend_pid();
                    """
                )
                self.conn.commit()
            logging.info("Deleted all connections")
        except Exception as e:
            logging.info(e)
            logging.info(
                "Could not connect to DB. Check if other connections are present or if DB exists."
            )
        finally:
            self.disconnect()

    def full_db_restore(self):
        logging.info("Killing all active database sessions...")
        # self.kill_all_db_sessions()
        # self.recreate_db()
        # self.disconnect()
        # logging.info("Downloading backup from S3...")
        # self.download_backup_from_s3(profile_name=os.getenv("AWS_PROFILE"))
        logging.info("Starting database restore...")
        start_time = time.time()
        self.restore_backup()
        end_time = time.time()
        elapsed = end_time - start_time
        logging.info(f"Database restored in {elapsed:.2f} seconds.")
