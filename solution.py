import re
import random
import psycopg2
from collections import Counter
import statistics
import math
from bs4 import BeautifulSoup 

class BincomPythonTest:
    def __init__(self, html_file=None):
        self.html_file = html_file
        self.colors = []
        self.color_counter = None
        
    def load_data(self):
        """Load color data from HTML file or use hardcoded data if file not available"""
        if self.html_file:
            try:
                self.colors = self.extract_colors_from_file(self.html_file)
            except Exception as e:
                print(f"Error loading from file: {e}")
                print("Falling back to hardcoded data...")
                self.colors = self.extract_colors_from_hardcoded()
        else:
            self.colors = self.extract_colors_from_hardcoded()
            
        # Calculate color frequencies once
        self.color_counter = Counter(self.colors)
        return len(self.colors)
        
    def extract_colors_from_file(self, file_path):
        """Extract colors from an HTML file"""
        with open(file_path, 'r') as file:
            html_content = file.read()
            
        # Use regex to extract color data from HTML
        pattern = r'<tr>\s*<td>([A-Z]+)</td>\s*<td>(.*?)</td>\s*</tr>'
        matches = re.findall(pattern, html_content, re.DOTALL)
        
        all_colors = []
        for day, colors_str in matches:
            # Split colors and clean them
            colors = [color.strip() for color in colors_str.split(',')]
            all_colors.extend(colors)
        
        return self._clean_colors(all_colors)
    
    def extract_colors_from_hardcoded(self):
        """Extract colors from hardcoded data"""
        color_data = {
            "MONDAY": "GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN",
            "TUESDAY": "ARSH, BROWN, GREEN, BROWN, BLUE, BLUE, BLEW, PINK, PINK, ORANGE, ORANGE, RED, WHITE, BLUE, WHITE, WHITE, BLUE, BLUE, BLUE",
            "WEDNESDAY": "GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, RED, YELLOW, ORANGE, RED, ORANGE, RED, BLUE, BLUE, WHITE, BLUE, BLUE, WHITE, WHITE",
            "THURSDAY": "BLUE, BLUE, GREEN, WHITE, BLUE, BROWN, PINK, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN",
            "FRIDAY": "GREEN, WHITE, GREEN, BROWN, BLUE, BLUE, BLACK, WHITE, ORANGE, RED, RED, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, WHITE"
        }
        
        all_colors = []
        for day, colors_str in color_data.items():
            colors = [color.strip() for color in colors_str.split(',')]
            all_colors.extend(colors)
        
        return self._clean_colors(all_colors)
    
    def _clean_colors(self, color_list):
        """Clean color data by fixing typos and removing blank entries"""
        cleaned_colors = []
        for color in color_list:
            # Fix known typos
            if color == "BLEW":
                color = "BLUE"
            elif color == "ARSH":
                color = "ASH"
            # Skip empty strings
            if color:
                cleaned_colors.append(color)
        
        return cleaned_colors
    
    def get_most_common_color(self):
        """Find the color worn most throughout the week"""
        most_common = self.color_counter.most_common(1)
        return most_common[0]
    
    def get_mean_color(self):
        """Find the mean color based on frequencies"""
        total_colors = len(self.colors)
        unique_colors = len(self.color_counter)
        mean_frequency = total_colors / unique_colors
        
        closest_color = None
        min_diff = float('inf')
        
        for color, freq in self.color_counter.items():
            diff = abs(freq - mean_frequency)
            if diff < min_diff:
                min_diff = diff
                closest_color = color
        
        return closest_color, mean_frequency
    
    def get_median_color(self):
        """Find the median color"""
        # Get all colors expanded by their frequencies
        expanded_colors = []
        for color, freq in self.color_counter.items():
            expanded_colors.extend([color] * freq)
        
        # Sort colors alphabetically to break ties consistently
        expanded_colors.sort()
        
        # Find the middle color
        n = len(expanded_colors)
        middle_idx = n // 2
        return expanded_colors[middle_idx]
    
    def get_color_variance(self):
        """Calculate variance of color frequencies"""
        frequencies = list(self.color_counter.values())
        return statistics.variance(frequencies) if len(frequencies) > 1 else 0
    
    def get_color_probability(self, target_color):
        """Calculate probability of randomly selecting a specific color"""
        target_count = self.color_counter.get(target_color.upper(), 0)
        return target_count / len(self.colors)
    
    def save_to_postgresql(self, dbname, user, password, host="localhost"):
        """Save color frequency data to PostgreSQL database"""
        try:
            # Connect to PostgreSQL
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host
            )
            
            # Create a cursor
            cur = conn.cursor()
            
            # Create table if it doesn't exist
            cur.execute("""
                CREATE TABLE IF NOT EXISTS color_frequencies (
                    id SERIAL PRIMARY KEY,
                    color VARCHAR(50) NOT NULL,
                    frequency INTEGER NOT NULL
                )
            """)
            
            # Clear existing data
            cur.execute("DELETE FROM color_frequencies")
            
            # Insert color frequencies
            for color, freq in self.color_counter.items():
                cur.execute(
                    "INSERT INTO color_frequencies (color, frequency) VALUES (%s, %s)",
                    (color, freq)
                )
            
            # Commit and close
            conn.commit()
            cur.close()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Database error: {e}")
            return False
    
    @staticmethod
    def recursive_search(numbers, target, start=0, end=None):
        """
        Recursive searching algorithm to search for a number in a list
        Uses binary search algorithm for efficiency
        """
        if end is None:
            end = len(numbers) - 1
        
        # Base case: empty list or sublist
        if start > end:
            return -1
        
        # Find middle index
        mid = (start + end) // 2
        
        # Check if middle element is the target
        if numbers[mid] == target:
            return mid
        
        # If target is smaller, search left sublist
        if numbers[mid] > target:
            return BincomPythonTest.recursive_search(numbers, target, start, mid - 1)
        
        # If target is larger, search right sublist
        return BincomPythonTest.recursive_search(numbers, target, mid + 1, end)
    
    @staticmethod
    def generate_binary_and_convert():
        """Generate random 4-digit binary number and convert to base 10"""
        # Generate 4 random binary digits
        binary_digits = [random.choice(['0', '1']) for _ in range(4)]
        binary_str = ''.join(binary_digits)
        
        # Convert to base 10
        decimal_value = int(binary_str, 2)
        
        return binary_str, decimal_value
    
    @staticmethod
    def sum_fibonacci(n=50):
        """Calculate sum of first n Fibonacci numbers"""
        if n <= 0:
            return 0
        
        # Initialize first two Fibonacci numbers
        a, b = 0, 1
        total_sum = b  # Start with F(1) = 1
        
        # Generate the Fibonacci sequence and sum
        for i in range(2, n+1):
            # Calculate next Fibonacci number
            a, b = b, a + b
            # Add to sum
            total_sum += b
        
        return total_sum
    
    def run_analysis(self):
        """Run all analysis tasks and print results"""
        print("=== Bincom Python Developer Test Solution ===\n")
        
        # Load color data
        total_colors = self.load_data()
        print(f"Total colors analyzed: {total_colors}")
        
        # Show color distribution
        print("\nColor distribution:")
        for color, count in sorted(self.color_counter.items(), key=lambda x: x[1], reverse=True):
            print(f"  {color}: {count}")
        
        print("\n=== Key Features Results ===")
        
        # 1. Find the mean color
        mean, mean_freq = self.get_mean_color()
        print(f"1. Mean color: {mean} (avg. frequency: {mean_freq:.2f})")
        
        # 2. Find the most worn color throughout the week
        most_worn, count = self.get_most_common_color()
        print(f"2. Most worn color: {most_worn} (worn {count} times)")
        
        # 3. Find the median color
        median = self.get_median_color()
        print(f"3. Median color: {median}")
        
        # 4. Calculate variance of the colors
        variance = self.get_color_variance()
        print(f"4. Variance of colors: {variance:.2f}")
        
        # 5. Calculate probability of randomly selecting red
        red_probability = self.get_color_probability("RED")
        print(f"5. Probability of randomly selecting RED: {red_probability:.4f} ({self.color_counter.get('RED', 0)} out of {total_colors})")
        
        # 6. Save to PostgreSQL (commented out to avoid connection errors)
        print("\n6. Saving color frequencies to PostgreSQL database...")
        success = self.save_to_postgresql("colour", "postgres", "Alliekundayo65")
        print(f"   {'Success!' if success else 'Failed to save to database.'}")
        
        # 7. Demonstrate recursive search algorithm
        print("\n7. Recursive search algorithm demonstration:")
        demo_list = sorted([13, 42, 7, 29, 56, 81, 23, 36, 91, 5])
        search_num = 29
        result = self.recursive_search(demo_list, search_num)
        print(f"   List: {demo_list}")
        print(f"   Searching for: {search_num}")
        print(f"   Result: Found at index {result}")
        
        # 8. Generate random binary number and convert to decimal
        binary, decimal = self.generate_binary_and_convert()
        print(f"\n8. Random 4-digit binary: {binary}, converted to decimal: {decimal}")
        
        # 9. Sum of first 50 Fibonacci numbers
        fib_sum = self.sum_fibonacci()
        print(f"\n9. Sum of first 50 Fibonacci numbers: {fib_sum}")


def analyze_binary_sequence_puzzle():
    print("\n=== Binary Sequence Analysis ===")
    input_sequence = "0101101011101011011101101000111"
    output_sequence = "0000000000100000000100000000001"
    
    print(f"Input:  {input_sequence}")
    print(f"Output: {output_sequence}")
    
    print("\nRule analysis: For every 1s that appear 3 times consecutively, the output will be 1, otherwise 0.")
    
    # Verify the rule
    calculated_output = ""
    for i in range(len(input_sequence) - 2):
        window = input_sequence[i:i+3]
        if window == "111":
            calculated_output += "1"
        else:
            calculated_output += "0"
    
    # Add zeroes at the end to match length (since we're using a 3-character window)
    calculated_output += "0" * 2
    
    print(f"Calculated: {calculated_output}")
    print(f"Matches expected output: {calculated_output == output_sequence}")

def main():
    test = BincomPythonTest(html_file="python_class_question.html")

    test.run_analysis()
    
    analyze_binary_sequence_puzzle()

if __name__ == "__main__":
    main()