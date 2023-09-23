import numpy as np
import commpy as cp


def ensure_no_reminder(x: int, y: int) -> bool:
    """
        Make sure that array with size x consists of exact 
        integer amount of y size array
    """
    if x and not x%y:
        return True
    return False


class TQAMModem(cp.QAMModem):
    def tmodulate(self, bits: np.ndarray) -> np.ndarray:        
        """
            The method only tested to work with bits arrays that consist of 1 and 0.
            The Modem also can moculate other numbers
        """
        if not ensure_no_reminder(bits.size, self.num_bits_symbol):
            raise ValueError(
                    f"{__class__.__name__} Error. Cannot modulate bit array with length {bits.size}"
                    f" by modem that requires {self.num_bits_symbol} bits per symbol"
                            )

        return self.modulate(bits)



if __name__ == '__main__':
    bits = np.random.randint(low=0, high=2, size=-1)
    qam4 = TQAMModem(16)
    moddata = qam4.tmodulate(bits)

    print(f'qam4.num_bits_symbol -> {qam4.num_bits_symbol}')
    print(f'bits.size -> {bits.size}')

