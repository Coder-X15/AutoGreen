from supabase.client import Client, create_client
from datetime import datetime

class DBAccessor:
    """
    Class to handle database access using Supabase.
    """
    def __init__(self, supabase_url: str, supabase_key: str):
        """
        Initialize the DBAccess with Supabase URL and Key.
        """
        self.supabase: Client = create_client(supabase_url, supabase_key)
        self.table_name = "greenhouse"

    def get_section_state(self, section_id: str):
        """
        Fetch data from a specified table.
        """
        response = self.supabase.table(self.table_name).select("*").eq("section", section_id).execute()
        if response.data:
            return response.data[0]
        else:
            raise RuntimeError(f"No such section with ID {section_id} found.")

    def water_section(self, section_id: str):
        """
        Update the state of a section to 'watered'.
        """
        try:
            self.supabase.table(self.table_name).update({"is_watered": True, "last_watered": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}).eq("section", section_id).execute()
        except Exception as e:
            raise RuntimeError(f"Failed to water section {section_id}: {str(e)}")