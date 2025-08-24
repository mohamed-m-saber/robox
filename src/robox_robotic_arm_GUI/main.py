#!/usr/bin/env python3
"""
Robox Robotics AI Kit Control Panel
Main entry point for the application
"""

import frontend


def main():
    """Main application entry point"""
    root = frontend.create_main_window()
    root.mainloop()


if __name__ == '__main__':
    main()