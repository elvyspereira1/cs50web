import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.safestring import mark_safe


def list_entries():
    """
    Returns a list of all names of encyclopedia entries as HTML links.
    """
    _, filenames = default_storage.listdir("entries")
    entries = sorted(re.sub(r"\.md$", "", filename)
                     for filename in filenames if filename.endswith(".md"))
    return [mark_safe(f"<a href='/wiki/{entry}'>{entry}</a>") for entry in entries]


def list_entries_clear():
    """
    Returns a list of all names of encyclopedia entries as HTML links.
    """
    _, filenames = default_storage.listdir("entries")
    entries = sorted(re.sub(r"\.md$", "", filename)
                     for filename in filenames if filename.endswith(".md"))
    return [f"{entry}" for entry in entries]


def list_search():
    """
    Returns a list of all names of encyclopedia entries as HTML links.
    """
    _, filenames = default_storage.listdir("entries")
    entries = sorted(re.sub(r"\.md$", "", filename)
                     for filename in filenames if filename.endswith(".md"))
    return [f"{entry}" for entry in entries]


def save_entry(title_original, content, title_new=None):
    """
    Saves an encyclopedia entry. If the entry is being renamed,
    it renames the file. Handles both new entries and updates.
    """
    title = title_new.strip() if title_new else title_original.strip()
    content_formatted = f"# {title}\n{content}"

    filename_original = f"entries/{title_original.strip()}.md"
    filename_new = f"entries/{title}.md"
    if title_new and title_new.strip() != title_original.strip():
        if default_storage.exists(filename_original):
            default_storage.delete(filename_original)

    if default_storage.exists(filename_new):
        default_storage.delete(filename_new)
    
    default_storage.save(filename_new, ContentFile(content_formatted.encode("utf-8")))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
