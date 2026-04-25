import operator
                                                                                                                      
def main():                                                                                                         
    print("--- Python 3.12 Lambda Function Examples ---")                                                           
                                                                                                                    
    # 1. Basic Addition                                                                                             
    add = lambda x, y: x + y                                                                                        
    print(f"1. Addition (5+3): {add(5, 3)}")                                                                        
                                                                                                                    
    # 2. Squaring a Number                                                                                          
    square = lambda x: x**2                                                                                         
    print(f"2. Square (4): {square(4)}")                                                                            
                                                                                                                    
    # 3. Conditional (Ternary) Expression                                                                           
    # Returns 'Even' if x % 2 == 0 else 'Odd'                                                                       
    check_even = lambda x: "Even" if x % 2 == 0 else "Odd"                                                          
    print(f"3. Parity (7): {check_even(7)}")                                                                        
                                                                                                                    
    # 4. Sorting a list of tuples by the second element                                                             
    pairs = [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]                                                     
    pairs.sort(key=lambda pair: pair[1])                                                                            
    print(f"4. Sorted tuples by name: {pairs}")                                                                     
                                                                                                                    
    # 5. Filtering a list (Keep only evens)                                                                         
    nums = [1, 2, 3, 4, 5, 6]                                                                                       
    evens = list(filter(lambda x: x % 2 == 0, nums))                                                                
    print(f"5. Filtered evens: {evens}")                                                                            
                                                                                                                    
    # 6. Mapping a function to a list (Double all numbers)                                                          
    doubled = list(map(lambda x: x * 2, nums))                                                                      
    print(f"6. Mapped doubles: {doubled}")                                                                          
                                                                                                                    
    # 7. Finding the max element based on a custom key (length of string)                                           
    words = ["apple", "banana", "cherry", "date"]                                                                   
    longest = max(words, key=lambda w: len(w))                                                                      
    print(f"7. Longest word: {longest}")                                                                            
                                                                                                                    
    # 8. Lambda inside another lambda (Currying)                                                                    
    multiplier = lambda x: lambda y: x * y                                                                          
    double_func = multiplier(2)                                                                                     
    print(f"8. Curried double (10): {double_func(10)}")                                                             
                                                                                                                    
    # 9. Sorting a dictionary by value                                                                              
    scores = {'Alice': 88, 'Bob': 95, 'Charlie': 80}                                                                
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)                                  
    print(f"9. Scores sorted desc: {sorted_scores}")                                                                
                                                                                                                    
    # 10. Simple string formatter                                                                                   
    greet = lambda name: f"Hello, {name}! Welcome to Ubuntu 24.04."                                                 
    print(f"10. Greeting: {greet('Developer')}")                                                                    
                                                                                                                    
    # 11. Extracting specific data from a list of dictionaries                                                      
    users = [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]                                                  
    names = list(map(lambda u: u['name'], users))                                                                   
    print(f"11. Extracted names: {names}")                                                                          
                                                                                                                    
    # 12. Summing a list using reduce (from functools)                                                              
    from functools import reduce                                                                                    
    total = reduce(lambda x, y: x + y, [1, 2, 3, 4])                                                                
    print(f"12. Reduce sum: {total}")                                                                               
                                                                                                                    
    # 13. Checking if a string is a palindrome                                                                      
    is_palindrome = lambda s: s == s[::-1]                                                                          
    print(f"13. Is 'radar' palindrome? {is_palindrome('radar')}")                                                   
                                                                                                                    
    # 14. Calculating the area of a circle (using math.pi)                                                          
    import math                                                                                                     
    circle_area = lambda r: math.pi * (r**2)                                                                        
    print(f"14. Circle area (r=5): {circle_area(5):.2f}")                                                           
                                                                                                                    
    # 15. Converting Celsius to Fahrenheit                                                                          
    c_to_f = lambda c: (c * 9/5) + 32                                                                               
    print(f"15. 25C to F: {c_to_f(25)}")                                                                            
                                                                                                                    
    # 16. Filtering a list of strings that start with a specific letter                                             
    fruit_list = ["apple", "apricot", "banana", "cherry"]                                                           
    a_fruits = list(filter(lambda f: f.startswith('a'), fruit_list))                                                
    print(f"16. Fruits starting with 'a': {a_fruits}")                                                              
                                                                                                                    
    # 17. Returning a list of squares using a list comprehension (implicitly using lambda-like logic)               
    # While not a lambda object, this is the "Pythonic" alternative to map(lambda...)                               
    squares_list = [ (lambda x: x**2)(x) for x in range(5) ]                                                        
    print(f"17. List comprehension lambda squares: {squares_list}")                                                 
                                                                                                                    
    # 18. Simple logic gate (AND)                                                                                   
    logic_and = lambda a, b: a and b                                                                                
    print(f"18. Logic AND (True, False): {logic_and(True, False)}")                                                 
                                                                                                                    
    # 19. Using lambda to create a quick function for a specific operator                                           
    # This is useful for generic mathematical utilities                                                             
    apply_op = lambda op, x, y: op(x, y)                                                                            
    print(f"19. Using operator.mul via lambda: {apply_op(operator.mul, 10, 5)}")                                    
                                                                                                                    
    # 20. Validating if a number is within a range                                                                  
    in_range = lambda x, start, end: start <= x <= end                                                              
    print(f"20. Is 15 in range 10-20? {in_range(15, 10, 20)}")                                                      
                                                                                                                    
if __name__ == "__main__":                                                                                          
    main()                                                                                                          
            
