"""
File Falcon Pro - Media organization utility.

This application helps organize media files by moving or copying them
based on file extension and other criteria.
"""
import logging
import sys

from PyQt6.QtWidgets import QApplication

from config import Config
from gui.main_window import MainWindow


def setup_logging() -> None:
    """Configure application logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("filefalpro.log", mode="a")
        ]
    )


def main() -> int:
    """Application entry point.
    
    Returns:
        Application exit code
    """
    # Setup logging
    setup_logging()
    logger = logging.getLogger("main")
    logger.info("Starting File Falcon Pro")
    
    # Create application configuration
    config = Config()
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("File Falcon Pro")
    app.setApplicationVersion("1.0.0")
    
    # Create and show main window
    main_window = MainWindow(config)
    main_window.show()
    
    # Run application event loop
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())