# 3. Longest_Substring Without Repeating Characters
# Given a string s, find the length of the longest substring without duplicate characters.
# Example 1:

# Input: s = "abcabcbb"
# Output: 3
# Explanation: The answer is "abc", with the length of 3. Note that "bca" and "cab" are also correct answers.
# Example 2:

# Input: s = "bbbbb"
# Output: 1
# Explanation: The answer is "b", with the length of 1.
# Example 3:

# Input: s = "pwwkew"
# Output: 3
# Explanation: The answer is "wke", with the length of 3.
# Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.


class Longest_Substring:
    def lengthOfLongestSubstring(self , s:str):
        substring_lengths={}
        len_s= len(s) #8 
        
        for i in range(len_s): #range(8) 0 to 7
            longest_string=s[i] # a s[0]
            print(substring_lengths)
            for j in range(i+1,len_s):
                if s[j] in longest_string:
                    break
                else :
                    longest_string=longest_string+s[j]
            substring_lengths[longest_string]= len(longest_string)
        print(substring_lengths)

        # Find the substring with the maximum length
        max_substring = max(substring_lengths, key=substring_lengths.get)
        max_length = substring_lengths[max_substring]

        print("All substrings and their lengths:", substring_lengths)
        print(f"Longest substring without repeating characters: '{max_substring}' (length {max_length})")
               

s1 = Longest_Substring()
s = "abcabcbb"
s1.lengthOfLongestSubstring(s)