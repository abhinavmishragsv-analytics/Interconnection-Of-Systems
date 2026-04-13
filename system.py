import numpy as np
import scipy.signal as sig

class System:
    """Continuous-time LTI system via transfer function H(s)."""

    def __init__(self, num, den, name="H(s)"):
        self.sys  = sig.TransferFunction(num, den)
        self.name = name
        self.num  = np.atleast_1d(num).astype(float)
        self.den  = np.atleast_1d(den).astype(float)

    def series(self, other):
        """H_eq = H1 * H2"""
        return System(np.polymul(self.num, other.num),
                      np.polymul(self.den, other.den),
                      f"{self.name} -> {other.name}")

    def parallel(self, other):
        """H_eq = H1 + H2"""
        num = np.polyadd(np.polymul(self.num, other.den),
                         np.polymul(other.num, self.den))
        return System(num, np.polymul(self.den, other.den),
                      f"{self.name} || {other.name}")

    def feedback(self, other=None, sign=-1):
        """H_eq = G / (1 +/- G*H)"""
        if other is None:
            fb_num = self.num
            fn = np.polyadd if sign == -1 else np.polysub
            fb_den = fn(self.den, self.num)
            label = f"UF({self.name})"
        else:
            H1H2_num = np.polymul(self.num, other.num)
            H1H2_den = np.polymul(self.den, other.den)
            fb_num   = np.polymul(self.num, other.den)
            fn = np.polyadd if sign == -1 else np.polysub
            fb_den = fn(H1H2_den, H1H2_num)
            label  = f"FB({'neg' if sign==-1 else 'pos'})({self.name})"
        return System(fb_num, fb_den, label)

    def bode(self, w):        return sig.bode(self.sys, w=w)
    def impulse_resp(self):   return sig.impulse(self.sys)
    def step_resp(self):      return sig.step(self.sys)
    def poles_zeros(self):    return np.roots(self.num), np.roots(self.den)
    
    def is_stable(self):
        _, poles = self.poles_zeros()
        if len(poles) == 0:
            return True
        return bool(np.all(poles.real < 0))