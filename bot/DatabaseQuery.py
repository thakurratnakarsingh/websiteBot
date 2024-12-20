from dbConfig import create_connection, close_connection

class DatabaseQuery:
    def __init__(self):
        self.connection = create_connection()

    def fetch_latest_entry(self):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = "SELECT * FROM h_s_m ORDER BY id DESC LIMIT 1"
                cursor.execute(query)
                result = cursor.fetchone()
                if result:
                    print(f"Latest Entry: ID: {result[0]}, Name: {result[1]}, IsCompleted: {result[2]}, MIS: {result[3]}")
                else:
                    print("No entries found in the h_s_m table.")
                return result  # Return the result for later use
            except Exception as e:
                print(f"An error occurred while fetching the latest entry: {e}")
        else:
            print("Failed to connect to the database.")
        return None

    def insert_entry(self, name, iscompleted, isDownload, isUploaded, download_url):
        """Inserts a new entry into the h_s_m table with the provided values."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = """
                INSERT INTO `h_s_m` (`name`, `iscompleted`, `isDownload`, `isUploaded`, `download_url`, `mis`)
                VALUES (%s, %s, %s, %s, %s, NULL)
                """
                cursor.execute(query, (name, iscompleted, isDownload, isUploaded, download_url))
                self.connection.commit()
                print(
                    f"Inserted entry: Name={name}, IsCompleted={iscompleted}, IsDownload={isDownload}, "
                    f"IsUploaded={isUploaded}, DownloadUrl={download_url}")
            except Exception as e:
                print(f"An error occurred during insertion: {e}")
        else:
            print("Failed to connect to the database.")

    def updateShortUrl(self, id, shortUrl):
        """Updates the shorten_url for a specific entry by ID."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = """
                         UPDATE `h_s_m` 
                         SET `shorten_url` = %s 
                         WHERE `id` = %s;
                         """
                # Execute the query with the correct parameters
                cursor.execute(query, (shortUrl, id))
                self.connection.commit()
                print(f"Updated entry: ID={id}, Shorten URL={shortUrl}")
            except Exception as e:
                print(f"An error occurred during update: {e}")
        else:
            print("Failed to connect to the database.")

    def updateIsCompleted(self, id, isCompleted):
        """Updates the shorten_url for a specific entry by ID."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = """
                         UPDATE `h_s_m` 
                         SET `iscompleted` = %s, 
                              `isUploaded` = %s
                         WHERE `id` = %s;
                         """
                # Execute the query with the correct parameters
                cursor.execute(query, (isCompleted, isCompleted, id))
                self.connection.commit()
                print(f"Updated entry: ID={id}, isUpload={isCompleted}")
            except Exception as e:
                print(f"An error occurred during update: {e}")
        else:
            print("Failed to connect to the database.")

    def close_connection(self):
        if self.connection:
            close_connection(self.connection)
            print("Database connection closed.")
        else:
            print("No active database connection to close.")
