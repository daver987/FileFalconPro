"""
File extension definitions for different media types.
This module provides categorized lists of file extensions for use in the File Falcon Pro application.
"""
from typing import Dict, List


def _normalize_extensions(extensions: List[str]) -> List[str]:
    """
    Convert a list of extensions to include both lowercase and uppercase variants.
    
    Args:
        extensions: List of file extensions in lowercase
        
    Returns:
        List containing both lowercase and uppercase variants
    """
    # Return unique extensions (no duplicates) in lowercase only
    # This is a better approach than manually including both cases
    return sorted(list(set([ext.lower() for ext in extensions])))


# Video file extensions
_VIDEO_ALL_RAW = [
    ".flv", ".webm", ".vob", ".avi", ".wmv", ".m4p", ".m4v", ".mpg", ".mpeg",
    ".3gp", ".mov", ".mp4", ".mkv", ".ogg", ".ogv", ".mts", ".m2ts", ".ts",
    ".qt", ".yuv", ".rm", ".rmvb", ".asf", ".amv", ".mpv", ".mpe", ".m2v"
]
video_all = _normalize_extensions(_VIDEO_ALL_RAW)

_VIDEO_BASIC_RAW = [
    ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".3gp", ".webm", ".mpg", ".vob"
]
video_basic = _normalize_extensions(_VIDEO_BASIC_RAW)

# Image file extensions
_IMAGE_BASIC_RAW = [
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".ico", ".jfif", ".webp", ".heic", ".svg"
]
image_basic = _normalize_extensions(_IMAGE_BASIC_RAW)

_IMAGE_ALL_RAW = _IMAGE_BASIC_RAW + [
    ".ai", ".eps", ".raw", ".indd", ".heif", ".pdf", ".psd", ".arw", ".cr2",
    ".nrw", ".k25", ".orf", ".raf", ".pef", ".x3f", ".srw", ".dng"
]
image_all = _normalize_extensions(_IMAGE_ALL_RAW)

# Document file extensions
_TEXT_RAW = [
    ".doc", ".docx", ".txt", ".odt", ".rtf", ".pages", ".wpd"
]
text = _normalize_extensions(_TEXT_RAW)

_SPREADSHEET_RAW = [
    ".xls", ".xlsx", ".ods", ".numbers", ".csv", ".tsv"
]
spreadsheet = _normalize_extensions(_SPREADSHEET_RAW)

_PRESENTATIONS_RAW = [
    ".ppt", ".pptx", ".odp", ".key", ".pps"
]
presentations = _normalize_extensions(_PRESENTATIONS_RAW)

_PDF_DOCUMENTS_RAW = [
    ".pdf"
]
pdf_documents = _normalize_extensions(_PDF_DOCUMENTS_RAW)

_JSON_DOCUMENTS_RAW = [
    ".json", ".jsonl"
]
json_documents = _normalize_extensions(_JSON_DOCUMENTS_RAW)

_LAYOUT_RAW = [
    ".indd", ".psd", ".ai", ".eps"
]
layout = _normalize_extensions(_LAYOUT_RAW)

_DATABASE_RAW = [
    ".db", ".sqlite", ".sqlite3", ".mdb", ".accdb"
]
database = _normalize_extensions(_DATABASE_RAW)

_DESIGN_RAW = [
    ".psd", ".ai", ".indd", ".xd", ".sketch", ".fig"
]
design = _normalize_extensions(_DESIGN_RAW)

_MARKUP_RAW = [
    ".html", ".htm", ".xml", ".svg", ".md", ".markdown"
]
markup = _normalize_extensions(_MARKUP_RAW)

# Create a mapping of categories to their extension lists for easy lookup
CATEGORIES_MAP: Dict[str, List[str]] = {
    "Video Basic": video_basic,
    "Video All": video_all,
    "Image Basic": image_basic,
    "Image All": image_all,
    "Text": text,
    "JSON": json_documents,
    "Spreadsheet": spreadsheet,
    "PDF": pdf_documents,
    "Presentations": presentations,
    "Layout": layout,
    "Database": database,
    "Design": design,
    "Markup": markup,
}
