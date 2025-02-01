# SnipBox
SnipBox is a short note-saving app that allows users to save text snippets and organize them with tags. This project is built using Django for the backend, Django Rest Framework (DRF) for API development, and SQLite as the database.
Features:

    Snippet Creation: Users can create short text snippets with a title, note content, and timestamps (created and updated times).
    User Association: Each snippet is linked to a user (creator) who is saved alongside the note.
    Tagging: Each snippet can be associated with tags. Tags are simple models with a title field, and tag titles must be unique.
    Tag Linking: Before creating a new tag, the system checks if a tag with the same title already exists. If it does, the snippet is linked to the existing tag instead of creating a new one.
    Authentication: JWT authentication is implemented to secure access to the API.

The app uses SQLite as the database for easy setup and local development.