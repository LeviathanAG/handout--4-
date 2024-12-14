import random
from sage.all import *

def decrypt_flag(out_file_path):
    """
    Attempts to decrypt the flag from an 'out' file.

    Args:
        out_file_path: Path to the 'out' file.

    Returns:
        A string representing the partially decrypted flag (or an empty string if decryption fails).
    """
    try:
        with open(out_file_path, 'r') as f:
            p = int(f.readline().strip())  # Read the prime number

            # Skip the line with the 'inp' list for now
            f.readline()

            # Read the 'out' list, processing each matrix
            out_matrices = []
            for line in f:
                if line.strip() == '[':
                    continue  # Skip lines with just '['
                elif line.strip() == ']':
                    break  # End of 'out' list
                else:
                    # Remove brackets, split into rows, then into elements
                    rows = line.strip().replace("[", "").replace("]", "").replace("),", ");").split(";")
                    matrix_data = [[int(val) for val in row.split(",")] for row in rows]
                    out_matrices.append(Matrix(GF(p), matrix_data))

    except FileNotFoundError:
        print(f"Error: File not found: {out_file_path}")
        return ""
    except Exception as e:
        print(f"Error reading or processing file: {e}")
        return ""

    # --- Analysis and Decryption Attempt (Similar to before, but with 'out' matrices) ---

    flag_bits = ""
    for M_out in out_matrices:
      try:
        # for each matrix we try to calculate M_out**(p//2)
        M_inv = M_out ** (p // 2)
        
        # we are only interested in the even powers so we take a sample of them.
        for power in range(4, 500, 2):
          M_in_candidate = M_inv ** (power // 2)

          # Check if the determinant is non-zero (invertible) and the rank is 2
          if M_in_candidate.determinant() != 0 and M_in_candidate.rank() == 2:
              flag_bit = "0" if power % 4 == 0 else "1"  # Example: Alternate bits based on power
              flag_bits += flag_bit
              break  # Move to the next matrix once a candidate is found
      except Exception as e:
        print(f"Error during analysis: {e}")
        continue

    print("Partially decrypted flag (bits):", flag_bits)
    return flag_bits

# --- Main execution ---

if __name__ == "__main__":
    out_file_path = "out"  # Replace with the actual path to your 'out' file
    decrypted_flag = decrypt_flag(out_file_path)
