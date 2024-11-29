import os
import shutil
import psutil
import tkinter as tk
from tkinter import messagebox, ttk
from plyer import notification
import pyttsx3
import speech_recognition as sr
import threading

class JarvisAssistant:
    def __init__(self, base_directory):
        self.base_directory = base_directory
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.wake_word = "jarvis"

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
            try:
                command = self.recognizer.recognize_google(audio)
                return command.lower()
            except sr.UnknownValueError:
                return None

    def continuous_listen(self):
        while True:
            command = self.listen()
            if command and self.wake_word in command:
                self.speak("Yes, sir. How can I assist you?")
                self.handle_command()

    def handle_command(self):
        command = self.listen()
        if command:
            if "optimize" in command:
                self.speak("Optimizing performance.")
                self.optimize_performance()
            elif "delete junk files" in command:
                self.speak("Deleting junk files.")
                self.delete_junk_files()
            elif "system diagnostics" in command:
                self.speak("Here are the system diagnostics.")
                self.monitor_system()
            elif "recommendations" in command:
                self.speak("Here are some recommendations.")
                self.provide_recommendations()
            else:
                self.speak("Sorry, I did not understand that command.")

    def organize_files_by_extension(self):
        for item in os.listdir(self.base_directory):
            item_path = os.path.join(self.base_directory, item)
            if os.path.isfile(item_path):
                extension = item.split('.')[-1]
                extension_dir = os.path.join(self.base_directory, extension)
                if not os.path.exists(extension_dir):
                    os.makedirs(extension_dir)
                shutil.move(item_path, os.path.join(extension_dir, item))

    def delete_empty_directories(self):
        for root, dirs, files in os.walk(self.base_directory, topdown=False):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)

    def list_large_files(self, size_threshold):
        large_files = []
        for root, dirs, files in os.walk(self.base_directory):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.getsize(file_path) > size_threshold:
                    large_files.append(file_path)
        return large_files

    def monitor_system(self):
        disk_usage = psutil.disk_usage(self.base_directory)
        self.speak(f"Disk usage is at {disk_usage.percent} percent.")
        return {'disk_usage': disk_usage}

    def alert_user(self, message):
        notification.notify(
            title='Jarvis Alert',
            message=message,
            app_name='Jarvis'
        )
        self.speak(message)

    def identify_junk_files(self):
        # Dummy implementation for example
        return ['file1.log', 'file2.tmp']

    def get_user_approval(self, junk_files):
        return messagebox.askyesno("Delete Junk Files", f"Do you want to delete these files?\n{junk_files}")

    def optimize_performance(self):
        self.organize_files_by_extension()
        self.delete_empty_directories()
        self.speak("System optimized for performance.")
        return "System optimized for performance."

    def delete_junk_files(self):
        junk_files = self.identify_junk_files()
        if junk_files:
            if self.get_user_approval(junk_files):
                for file in junk_files:
                    os.remove(file)
                self.alert_user("Junk files deleted")
            else:
                self.alert_user("Junk files not deleted")

    def provide_recommendations(self):
        recommendations = [
            "1. Consider deleting large files to free up space.",
            "2. Regularly clean up junk files.",
            "3. Organize files by extension for better management."
        ]
        for recommendation in recommendations:
            self.speak(recommendation)

def main():
    assistant = JarvisAssistant(base_directory="C:/Users/pkswa")

    # Start continuous listening in a background thread
    threading.Thread(target=assistant.continuous_listen, daemon=True).start()

    # Create the main window
    root = tk.Tk()
    root.title("Jarvis - AI Assistant")
    root.geometry("800x600")

    # Create a notebook (tabbed interface)
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Create frames for each tab
    home_frame = ttk.Frame(notebook, padding="10")
    diagnostics_frame = ttk.Frame(notebook, padding="10")
    recommendations_frame = ttk.Frame(notebook, padding="10")
    notebook.add(home_frame, text="Home")
    notebook.add(diagnostics_frame, text="Diagnostics")
    notebook.add(recommendations_frame, text="Recommendations")

    # Home Tab
    home_label = ttk.Label(home_frame, text="Welcome to Jarvis", font=("Helvetica", 16))
    home_label.pack(pady=10)

    optimize_button = ttk.Button(home_frame, text="Optimize Performance", command=lambda: messagebox.showinfo("Optimization", assistant.optimize_performance()))
    optimize_button.pack(pady=10)

    delete_junk_button = ttk.Button(home_frame, text="Delete Junk Files", command=assistant.delete_junk_files)
    delete_junk_button.pack(pady=10)

    speak_button = ttk.Button(home_frame, text="Speak", command=lambda: assistant.speak("Hello, how can I assist you today?"))
    speak_button.pack(pady=10)

    listen_button = ttk.Button(home_frame, text="Listen", command=lambda: assistant.listen())
    listen_button.pack(pady=10)

    # Diagnostics Tab
    diagnostics_label = ttk.Label(diagnostics_frame, text="System Diagnostics", font=("Helvetica", 16))
    diagnostics_label.pack(pady=10)

    # Disk usage monitoring
    system_info = assistant.monitor_system()
    disk_usage_label = ttk.Label(diagnostics_frame, text=f"Disk Usage: {system_info['disk_usage'].percent}%")
    disk_usage_label.pack(pady=5)

    if system_info['disk_usage'].percent > 80:
        assistant.alert_user("Disk usage is above 80%")

    # Organize files by extension
    assistant.organize_files_by_extension()

    # Delete empty directories
    assistant.delete_empty_directories()

    # List large files
    size_threshold = 100 * 1024 * 1024  # 100 MB
    large_files = assistant.list_large_files(size_threshold)

    # Display large files in the GUI
    large_files_label = ttk.Label(diagnostics_frame, text="Large files:")
    large_files_label.pack(pady=5)

    large_files_listbox = tk.Listbox(diagnostics_frame)
    large_files_listbox.pack(fill=tk.BOTH, expand=True)
    for file in large_files:
        large_files_listbox.insert(tk.END, file)

    # Recommendations Tab
    recommendations_label = ttk.Label(recommendations_frame, text="AI Recommendations", font=("Helvetica", 16))
    recommendations_label.pack(pady=10)

    recommendations_text = tk.Text(recommendations_frame, wrap=tk.WORD, height=15)
    recommendations_text.pack(fill=tk.BOTH, expand=True)
    recommendations_text.insert(tk.END, "1. Consider deleting large files to free up space.\n")
    recommendations_text.insert(tk.END, "2. Regularly clean up junk files.\n")
    recommendations_text.insert(tk.END, "3. Organize files by extension for better management.\n")

    root.mainloop()

if __name__ == "__main__":
    main()