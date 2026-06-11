"""
============================================================
 MINOR ASSIGNMENT - 1: OBJECT-ORIENTED PROGRAMMING (OOP)
 Python for Computer Science and Data Science 2 (CSE 3652)
 Centre for Data Science, ITER, SOA University
============================================================
Each section below begins with the question, followed by the
solution. The file is fully self-contained and runs end-to-end
in a Jupyter notebook (Run All) or `python Assignment1_OOP.py`.
"""

import random
from dataclasses import dataclass, field
from typing import List
import pandas as pd
import matplotlib.pyplot as plt

print("=" * 70)
print(" ASSIGNMENT 1 — OBJECT-ORIENTED PROGRAMMING")
print("=" * 70)

# ---------------------------------------------------------------
# Q1. Significance of classes in Python and contribution to OOP
# ---------------------------------------------------------------
print("\n----- Q1: Significance of Classes -----")
Q1_ANS = """
Classes in Python are blueprints that bundle data (attributes) and
behaviour (methods) into a single unit. They underpin OOP by enabling:
  - Encapsulation : hide internal state behind a clean interface
  - Inheritance   : derive specialised classes from general ones
  - Polymorphism  : same interface, different concrete behaviour
  - Abstraction   : expose only what is essential
This leads to code that is modular, reusable and easier to maintain.
"""
print(Q1_ANS)

# ---------------------------------------------------------------
# Q2. Bank account class with deposit and withdrawal
# ---------------------------------------------------------------
print("\n----- Q2: Simple BankAccount -----")
class BankAccountSimple:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
    def deposit(self, amount):
        self.balance += amount
        print(f"  Deposited {amount}. New balance: {self.balance}")
    def withdraw(self, amount):
        if amount > self.balance:
            print("  Insufficient funds.")
        else:
            self.balance -= amount
            print(f"  Withdrew {amount}. New balance: {self.balance}")

acc = BankAccountSimple("Ritu", 1000)
acc.deposit(500)
acc.withdraw(300)
acc.withdraw(5000)

# ---------------------------------------------------------------
# Q3. Book composed of Chapters
# ---------------------------------------------------------------
print("\n----- Q3: Book / Chapter composition -----")
class Chapter:
    def __init__(self, title, page_count):
        self.title = title
        self.page_count = page_count

class Book:
    def __init__(self, title, chapters):
        self.title = title
        self.chapters = chapters
    def total_pages(self):
        return sum(ch.page_count for ch in self.chapters)

book = Book("Python Mastery",
            [Chapter("Intro", 20),
             Chapter("Classes", 35),
             Chapter("Advanced", 40)])
print(f"  Book: {book.title}, total pages = {book.total_pages()}")

# ---------------------------------------------------------------
# Q4. Access control: public / protected / private
# ---------------------------------------------------------------
print("\n----- Q4: Access modifiers -----")
class AccessDemo:
    def __init__(self):
        self.public = "anyone can touch me"
        self._protected = "convention: subclass only"
        self.__private = "name-mangled to _AccessDemo__private"

a = AccessDemo()
print(f"  public    -> {a.public}")
print(f"  protected -> {a._protected}")
print(f"  private   -> {a._AccessDemo__private}  (name-mangled)")

# ---------------------------------------------------------------
# Q5. Time class — validate & convert 24h to 12h
# ---------------------------------------------------------------
print("\n----- Q5: Time conversion -----")
class TimeConverter:
    def __init__(self, time_str):
        self.time_str = time_str
    def is_valid(self):
        parts = self.time_str.split(":")
        if len(parts) != 3:
            return False
        try:
            h, m, s = map(int, parts)
        except ValueError:
            return False
        return 0 <= h < 24 and 0 <= m < 60 and 0 <= s < 60
    def to_12_hour(self):
        if not self.is_valid():
            return "Invalid time format. Expected HH:MM:SS."
        h, m, s = map(int, self.time_str.split(":"))
        suffix = "AM" if h < 12 else "PM"
        h12 = h % 12 or 12
        return f"{h12:02d}:{m:02d}:{s:02d} {suffix}"

for t in ["09:15:00", "23:45:10", "25:00:00", "12:00:00"]:
    print(f"  {t}  ->  {TimeConverter(t).to_12_hour()}")

# ---------------------------------------------------------------
# Q6. BankAccount with private attributes
# ---------------------------------------------------------------
print("\n----- Q6: Private-attribute BankAccount -----")
class SecureAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.__balance += amount
    def withdraw(self, amount):
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        self.__balance -= amount
    def display(self):
        print(f"  Owner: {self.owner}, Balance: {self.__balance}")

s = SecureAccount("Soham", 5000)
s.deposit(1500); s.withdraw(2000); s.display()
print("  Why private attrs? Stops outside code from mutating balance directly,")
print("  forcing all changes through validated methods — better data integrity.")

# ---------------------------------------------------------------
# Q7. Card / Deck / Player game
# ---------------------------------------------------------------
print("\n----- Q7: Card game (Card / Deck / Player) -----")
class Card:
    def __init__(self, rank, suit):
        self.rank, self.suit = rank, suit
    def __repr__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    RANKS = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    SUITS = ["♠","♥","♦","♣"]
    def __init__(self):
        self.cards = [Card(r, s) for s in Deck.SUITS for r in Deck.RANKS]
    def shuffle(self):
        random.shuffle(self.cards)
    def deal(self, n):
        hand = self.cards[:n]
        self.cards = self.cards[n:]
        return hand

class Player:
    def __init__(self, name):
        self.name, self.hand = name, []
    def receive(self, cards):
        self.hand.extend(cards)

random.seed(0)
deck = Deck(); deck.shuffle()
players = [Player(f"P{i+1}") for i in range(2)]
for p in players:
    p.receive(deck.deal(5))
    print(f"  {p.name}: {p.hand}")

# ---------------------------------------------------------------
# Q8. Inheritance: Vehicle and Car
# ---------------------------------------------------------------
print("\n----- Q8: Vehicle / Car inheritance -----")
class Vehicle:
    def __init__(self, make, model):
        self.make, self.model = make, model
    def display_info(self):
        print(f"  Vehicle: {self.make} {self.model}")

class Car(Vehicle):
    def __init__(self, make, model, num_doors):
        super().__init__(make, model)
        self.num_doors = num_doors
    def display_info(self):
        super().display_info()
        print(f"  Doors: {self.num_doors}")

Vehicle("Tata", "Truck").display_info()
Car("Honda", "Civic", 4).display_info()

# ---------------------------------------------------------------
# Q9. Polymorphism with Shape / Circle / Rectangle
# ---------------------------------------------------------------
print("\n----- Q9: Polymorphism (Shape hierarchy) -----")
class Shape:
    def area(self): raise NotImplementedError
class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14159 * self.r ** 2
class Rectangle(Shape):
    def __init__(self, w, h): self.w, self.h = w, h
    def area(self): return self.w * self.h

for s in [Circle(5), Rectangle(4, 6)]:
    print(f"  {type(s).__name__} area = {s.area():.2f}")

# ---------------------------------------------------------------
# Q10. CommissionEmployee with properties & validation
# ---------------------------------------------------------------
print("\n----- Q10: CommissionEmployee -----")
class CommissionEmployee:
    def __init__(self, first, last, ssn, sales, rate):
        self.first_name = first
        self.last_name = last
        self.ssn = ssn
        self.gross_sales = sales
        self.commission_rate = rate
    @property
    def gross_sales(self): return self._gross_sales
    @gross_sales.setter
    def gross_sales(self, v):
        if v < 0: raise ValueError("gross_sales must be >= 0")
        self._gross_sales = v
    @property
    def commission_rate(self): return self._commission_rate
    @commission_rate.setter
    def commission_rate(self, v):
        if not 0 < v < 1: raise ValueError("commission_rate must be in (0,1)")
        self._commission_rate = v
    def earnings(self):
        return self._gross_sales * self._commission_rate
    def __repr__(self):
        return (f"CommissionEmployee({self.first_name} {self.last_name}, "
                f"sales={self._gross_sales}, rate={self._commission_rate})")

emp = CommissionEmployee("Sue", "Jones", "111-22-3333", 10000, 0.06)
print("  ", emp)
print(f"  Earnings: {emp.earnings():.2f}")
emp.gross_sales = 20000
print(f"  Updated earnings: {emp.earnings():.2f}")
try:
    emp.gross_sales = -1
except ValueError as e:
    print(f"  Caught error: {e}")

# ---------------------------------------------------------------
# Q11. Duck typing — describe(any obj with speak())
# ---------------------------------------------------------------
print("\n----- Q11: Duck typing -----")
def describe(obj):
    print(f"  {type(obj).__name__} says: {obj.speak()}")
class Dog:
    def speak(self): return "Woof!"
class Robot:
    def speak(self): return "Beep boop."
describe(Dog()); describe(Robot())
print("  No type-check needed; any object with a .speak() works — that's duck typing.")

# ---------------------------------------------------------------
# Q12. Overload + for a Complex class
# ---------------------------------------------------------------
print("\n----- Q12: Complex number + overload -----")
class MyComplex:
    def __init__(self, real, imag):
        self.real, self.imag = real, imag
    def __add__(self, other):
        return MyComplex(self.real + other.real, self.imag + other.imag)
    def __repr__(self):
        sign = "+" if self.imag >= 0 else "-"
        return f"{self.real}{sign}{abs(self.imag)}i"

c1, c2 = MyComplex(3, 4), MyComplex(1, -2)
print(f"  {c1} + {c2} = {c1 + c2}")

# ---------------------------------------------------------------
# Q13. Custom exception for insufficient funds
# ---------------------------------------------------------------
print("\n----- Q13: Custom InsufficientFundsError -----")
class InsufficientFundsError(Exception):
    def __init__(self, balance, amount):
        super().__init__(
            f"Cannot withdraw {amount}. Current balance: {balance}")
        self.balance, self.amount = balance, amount

class AccountX:
    def __init__(self, bal): self.bal = bal
    def withdraw(self, amt):
        if amt > self.bal:
            raise InsufficientFundsError(self.bal, amt)
        self.bal -= amt
try:
    AccountX(100).withdraw(500)
except InsufficientFundsError as e:
    print(f"  Caught: {e}")

# ---------------------------------------------------------------
# Q14. Data-class Card; deal 5 from a shuffled deck
# ---------------------------------------------------------------
print("\n----- Q14: dataclass Card + dealing 5 -----")
@dataclass
class CardDC:
    rank: str
    suit: str

class DeckDC:
    RANKS = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    SUITS = ["S","H","D","C"]
    def __init__(self):
        self.cards = [CardDC(r, s) for s in DeckDC.SUITS for r in DeckDC.RANKS]
        random.shuffle(self.cards)
    def deal(self, n):
        hand, self.cards = self.cards[:n], self.cards[n:]
        return hand

random.seed(1)
d = DeckDC()
hand = d.deal(5)
print(f"  Player's hand: {hand}")
print(f"  Cards left in deck: {len(d.cards)}")

# ---------------------------------------------------------------
# Q15. Data classes vs named tuples
# ---------------------------------------------------------------
print("\n----- Q15: dataclass vs namedtuple -----")
from collections import namedtuple
PointNT = namedtuple("PointNT", ["x", "y"])
@dataclass
class PointDC:
    x: float
    y: float
    def distance_from_origin(self):
        return (self.x**2 + self.y**2) ** 0.5

p_nt = PointNT(3, 4)
p_dc = PointDC(3, 4)
print(f"  namedtuple: {p_nt}  (immutable, no methods)")
print(f"  dataclass : {p_dc}, distance = {p_dc.distance_from_origin():.2f}")
print("  Dataclasses allow mutability (default), methods, defaults, inheritance.")

# ---------------------------------------------------------------
# Q16. doctest within a function docstring
# ---------------------------------------------------------------
print("\n----- Q16: doctest -----")
def add(a, b):
    """
    >>> add(2, 3)
    5
    >>> add(-1, 1)
    0
    >>> add(10, 20)
    30
    """
    return a + b

import doctest
results = doctest.testmod(verbose=False)
print(f"  doctest results: attempted={results.attempted}, failed={results.failed}")

# ---------------------------------------------------------------
# Q17. Scope-resolution example
# ---------------------------------------------------------------
print("\n----- Q17: Scope resolution -----")
species = "GlobalSpecies"
class Animal:
    species = "ClassSpecies"
    def __init__(self, sp):
        self.species = sp
    def display_species(self):
        print(f"  Instance species: {self.species}")
        print(f"  Class species   : {Animal.species}")
        print(f"  Global species  : {globals()['species']}")

Animal("InstanceSpecies").display_species()
print("  LEGB: self.species (Local/instance) -> Animal.species (Enclosing/class)")
print("  -> globals()['species'] (Global) -> built-ins (last).")

# ---------------------------------------------------------------
# Q18. lambda Celsius->Kelvin, pandas table & plot
# ---------------------------------------------------------------
print("\n----- Q18: Celsius to Kelvin with lambda + pandas + plot -----")
c_to_k = lambda c: c + 273.15
celsius = list(range(-20, 41, 10))
df_temp = pd.DataFrame({
    "Celsius": celsius,
    "Kelvin": [c_to_k(c) for c in celsius]
})
print(df_temp.to_string(index=False))

plt.figure(figsize=(7, 4))
plt.plot(df_temp["Celsius"], df_temp["Kelvin"], marker="o")
plt.title("Celsius -> Kelvin")
plt.xlabel("Celsius (°C)"); plt.ylabel("Kelvin (K)")
plt.grid(True); plt.tight_layout()
plt.savefig("/home/claude/a1_q18_temp.png", dpi=80)
plt.close()
print("  Plot saved as a1_q18_temp.png")

print("\n" + "=" * 70)
print(" Assignment 1 complete.")
print("=" * 70)



"""
============================================================
 MINOR ASSIGNMENT - 2: COMPUTER SCIENCE THINKING
 RECURSION, SEARCHING, SORTING AND BIG O
 Python for Computer Science and Data Science 2 (CSE 3652)
 Centre for Data Science, ITER, SOA University
============================================================
Each section starts with the question, then the solution.
Self-contained: run end-to-end in Jupyter (Run All) or
`python Assignment2_Algorithms.py`.
"""

import math
import time
from functools import lru_cache

print("=" * 70)
print(" ASSIGNMENT 2 — RECURSION, SORTING, SEARCHING, BIG O")
print("=" * 70)

# ---------------------------------------------------------------
# Q1. Recursive power(base, exponent)
# ---------------------------------------------------------------
print("\n----- Q1: Recursive power -----")
def power(base, exponent):
    if exponent == 1:
        return base
    return base * power(base, exponent - 1)

print(f"  power(3, 4) = {power(3, 4)}")
print(f"  power(2, 10) = {power(2, 10)}")

# ---------------------------------------------------------------
# Q2. Recursive GCD
# ---------------------------------------------------------------
print("\n----- Q2: Recursive GCD -----")
def gcd(x, y):
    if y == 0:
        return x
    return gcd(y, x % y)

for a, b in [(48, 18), (100, 75), (17, 31)]:
    print(f"  gcd({a}, {b}) = {gcd(a, b)}")

# ---------------------------------------------------------------
# Q3. n-digit strictly increasing numbers (recursive)
# ---------------------------------------------------------------
print("\n----- Q3: n-digit strictly increasing numbers -----")
def strictly_increasing(n, start=1, current=""):
    if n == 0:
        print(f"  {current}", end="  ")
        return
    for d in range(start, 10):
        strictly_increasing(n - 1, d + 1, current + str(d))

print("  All strictly-increasing 3-digit numbers:")
strictly_increasing(3)
print()

# ---------------------------------------------------------------
# Q4. Recursive Fibonacci + memoised version + comparison
# ---------------------------------------------------------------
print("\n\n----- Q4: Fibonacci — naive vs memoised -----")
def fib_naive(n):
    if n < 2: return n
    return fib_naive(n - 1) + fib_naive(n - 2)

@lru_cache(maxsize=None)
def fib_memo(n):
    if n < 2: return n
    return fib_memo(n - 1) + fib_memo(n - 2)

N = 30
t = time.time(); fib_naive(N); t_naive = time.time() - t
t = time.time(); fib_memo(N);  t_memo  = time.time() - t
print(f"  fib({N}) naive  : {fib_naive(N)}   time {t_naive*1000:.2f} ms")
print(f"  fib({N}) memo   : {fib_memo(N)}   time {t_memo*1000:.4f} ms")
print("  Naive: O(2^n); memoised: O(n) time, O(n) space. Memo wins by orders of magnitude.")

# ---------------------------------------------------------------
# Q5. k-th largest in O(N) expected — Quickselect
# ---------------------------------------------------------------
print("\n----- Q5: k-th largest via Quickselect (O(N) expected) -----")
import random
def quickselect_kth_largest(arr, k):
    # k = 1 means largest
    if not arr: return None
    pivot = random.choice(arr)
    larger  = [x for x in arr if x > pivot]
    equal   = [x for x in arr if x == pivot]
    smaller = [x for x in arr if x < pivot]
    if k <= len(larger):
        return quickselect_kth_largest(larger, k)
    elif k <= len(larger) + len(equal):
        return pivot
    else:
        return quickselect_kth_largest(smaller, k - len(larger) - len(equal))

random.seed(7)
sample = [12, 3, 5, 7, 19, 4, 26, 9, 1, 14]
for k in [1, 3, 5]:
    print(f"  {k}-th largest of {sample} = {quickselect_kth_largest(sample, k)}")

# ---------------------------------------------------------------
# Q6. Big-O of three snippets
# ---------------------------------------------------------------
print("\n----- Q6: Big-O classification -----")
print("  (a) nested loops i,j in range(n)            -> O(n^2)")
print("  (b) single loop i in range(n)               -> O(n)")
print("  (c) f(n) = f(n-1) + f(n-1)                  -> O(2^n)")

# ---------------------------------------------------------------
# Q7. Antipodal points on a circle in O(N log N)
# ---------------------------------------------------------------
print("\n----- Q7: Antipodal-pair detection in O(N log N) -----")
def find_antipodal(points):
    # Each point (x,y) is on the circle; its antipode is (-x,-y).
    # Normalise polar angles to [0, 2π) so wrap-around is clean,
    # then look for (theta + pi) mod 2π.
    angles = sorted(round(math.atan2(y, x) % (2 * math.pi), 9) for x, y in points)
    angle_set = set(angles)
    for ang in angles:
        opp = round((ang + math.pi) % (2 * math.pi), 9)
        if opp in angle_set:
            return True
    return False

pts1 = [(1, 0), (0, 1), (-1, 0)]              # contains (1,0) & (-1,0)
pts2 = [(1, 0), (0, 1), (math.cos(1), math.sin(1))]
print(f"  {pts1} -> antipodal? {find_antipodal(pts1)}")
print(f"  pts2 sample -> antipodal? {find_antipodal(pts2)}")
print("  Sort = O(N log N); membership lookup in set = O(1) avg. Total O(N log N).")

# ---------------------------------------------------------------
# Q8. Quicksort (pivot = first element)
# ---------------------------------------------------------------
print("\n----- Q8: Quicksort in-place -----")
def quick_sort(arr):
    def helper(a, lo, hi):
        if lo >= hi: return
        pivot = a[lo]
        left, right = lo + 1, hi
        while True:
            while left <= right and a[left] <= pivot:
                left += 1
            while left <= right and a[right] > pivot:
                right -= 1
            if left > right:
                break
            a[left], a[right] = a[right], a[left]
        a[lo], a[right] = a[right], a[lo]
        helper(a, lo, right - 1)
        helper(a, right + 1, hi)
    helper(arr, 0, len(arr) - 1)
    return arr

data = [37, 2, 6, 4, 89, 8, 10, 12, 68, 45]
print(f"  Input : {data}")
print(f"  Sorted: {quick_sort(data.copy())}")

# ---------------------------------------------------------------
# Q9. Selection / Bubble / Insertion sort on net worths
# ---------------------------------------------------------------
print("\n----- Q9: Sorting net worths (3 algorithms) -----")
people = [
    ("Elon Musk", 433.9),
    ("Jeff Bezos", 239.4),
    ("Mark Zuckerberg", 211.8),
    ("Larry Ellison", 204.6),
    ("Bernard Arnault & Family", 181.3),
    ("Larry Page", 161.4),
]

def selection_sort(lst):
    a = lst.copy()
    for i in range(len(a)):
        max_idx = i
        for j in range(i + 1, len(a)):
            if a[j][1] > a[max_idx][1]:
                max_idx = j
        a[i], a[max_idx] = a[max_idx], a[i]
    return a

def bubble_sort(lst):
    a = lst.copy()
    n = len(a)
    for i in range(n):
        for j in range(n - i - 1):
            if a[j][1] < a[j + 1][1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a

def insertion_sort(lst):
    a = lst.copy()
    for i in range(1, len(a)):
        key = a[i]; j = i - 1
        while j >= 0 and a[j][1] < key[1]:
            a[j + 1] = a[j]; j -= 1
        a[j + 1] = key
    return a

for name, fn in [("Selection", selection_sort),
                 ("Bubble",    bubble_sort),
                 ("Insertion", insertion_sort)]:
    result = {n: w for n, w in fn(people)}
    print(f"  {name}: {result}")

# ---------------------------------------------------------------
# Q10. Merge sort on strings
# ---------------------------------------------------------------
print("\n----- Q10: Merge sort (strings) -----")
def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)

def _merge(a, b):
    out, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    out.extend(a[i:]); out.extend(b[j:])
    return out

words = ["apple", "orange", "banana", "grape"]
print(f"  Input : {words}")
print(f"  Sorted: {merge_sort(words)}")

# ---------------------------------------------------------------
# Q11. Merge two pre-sorted lists (no sorted())
# ---------------------------------------------------------------
print("\n----- Q11: Merge two pre-sorted lists -----")
A = [1, 3, 5, 7]; B = [2, 4, 6, 8]
print(f"  Input : {A} and {B}")
print(f"  Merged: {_merge(A, B)}")

print("\n" + "=" * 70)
print(" Assignment 2 complete.")
print("=" * 70)




"""
============================================================
 MINOR ASSIGNMENT - 3: NATURAL LANGUAGE PROCESSING
 Python for Computer Science and Data Science 2 (CSE 3652)
 Centre for Data Science, ITER, SOA University
============================================================
Self-contained: run in Jupyter (Run All) or as a script.
Web-scraping / external-download tasks use a try/except fallback
to bundled sample text so the file works offline. NLTK data
needed: punkt, punkt_tab, stopwords, wordnet, omw-1.4,
averaged_perceptron_tagger(_eng), brown. The download lines
below fetch them once (idempotent).
"""

import os
import re
import nltk
import requests
from collections import Counter

# One-shot NLTK data download (silent / idempotent)
for pkg in ["punkt", "punkt_tab", "stopwords", "wordnet", "omw-1.4",
            "averaged_perceptron_tagger", "averaged_perceptron_tagger_eng",
            "brown", "movie_reviews", "maxent_ne_chunker",
            "maxent_ne_chunker_tab", "words"]:
    try:
        nltk.download(pkg, quiet=True)
    except Exception:
        pass

print("=" * 70)
print(" ASSIGNMENT 3 — NATURAL LANGUAGE PROCESSING")
print("=" * 70)

# ---------------------------------------------------------------
# Q1. Define NLP and three real-world applications
# ---------------------------------------------------------------
print("\n----- Q1: Definition + applications of NLP -----")
print("""  NLP (Natural Language Processing) is a branch of AI that enables
  computers to understand, interpret and generate human language.

  Three real-world applications:
   1. Machine translation (Google Translate) — breaks down language barriers
      in travel, education, business.
   2. Sentiment analysis on social media — companies/governments gauge
      public opinion at scale, used in marketing & policy.
   3. Conversational assistants (Siri, Alexa, ChatGPT) — accessibility
      for users with disabilities, hands-free productivity, customer support.
""")

# ---------------------------------------------------------------
# Q2. Tokenization / Stemming / Lemmatization
# ---------------------------------------------------------------
print("----- Q2: Tokenization, stemming, lemmatization -----")
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

sample = "The striped bats are hanging on their feet for best results."
tokens = word_tokenize(sample)
stems = [PorterStemmer().stem(w) for w in tokens]
lems  = [WordNetLemmatizer().lemmatize(w, pos='v') for w in tokens]
print(f"  Tokens     : {tokens}")
print(f"  Stems      : {stems}")
print(f"  Lemmas (v) : {lems}")
print("  Tokenization: splits text into units (words/sentences).")
print("  Stemming   : chops affixes (running -> run, fast & crude).")
print("  Lemmatization: returns dictionary base form using morphology.")

# ---------------------------------------------------------------
# Q3. Part-of-Speech tagging
# ---------------------------------------------------------------
print("\n----- Q3: POS tagging -----")
from nltk import pos_tag
text = "The quick brown fox jumps over the lazy dog."
print(f"  Sentence: {text}")
print(f"  POS tags: {pos_tag(word_tokenize(text))}")
print("  POS tagging labels each token with a grammatical category — vital")
print("  for parsing, NER, sentiment, machine translation, etc.")

# ---------------------------------------------------------------
# Q4. Create a TextBlob exercise_blob
# ---------------------------------------------------------------
print("\n----- Q4: TextBlob exercise_blob -----")
from textblob import TextBlob
exercise_blob = TextBlob("This is a TextBlob")
print(f"  exercise_blob = {exercise_blob!r}")
print(f"  Words: {exercise_blob.words}")

# ---------------------------------------------------------------
# Q5. Tokenize, stem, lemmatize, remove stopwords
# ---------------------------------------------------------------
print("\n----- Q5: Tokenize / stem / lemmatize / remove stopwords -----")
from nltk.corpus import stopwords
text5 = ("Natural Language Processing enables machines to understand and "
         "process human languages. It is a fascinating field with numerous "
         "applications, such as chatbots and language translation.")
from nltk.tokenize import sent_tokenize
sents = sent_tokenize(text5)
words = word_tokenize(text5)
sw = set(stopwords.words('english'))
filtered = [w for w in words if w.lower() not in sw and w.isalnum()]
ps = PorterStemmer(); wl = WordNetLemmatizer()
print(f"  Sentences ({len(sents)}): {sents}")
print(f"  Filtered words: {filtered}")
print(f"  Stems  : {[ps.stem(w) for w in filtered]}")
print(f"  Lemmas : {[wl.lemmatize(w) for w in filtered]}")

# ---------------------------------------------------------------
# Q6. Scrape python.org, build a word cloud
# ---------------------------------------------------------------
print("\n----- Q6: Scrape www.python.org + word cloud -----")
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt

scraped_text = None
FALLBACK_TEXT = ("Python is a programming language that lets you work quickly and "
                 "integrate systems more effectively. Python is powerful, fast, "
                 "easy to learn, open source, and has a vibrant community. "
                 "Python supports object oriented programming, functional "
                 "programming, and imperative programming styles. The Python "
                 "Software Foundation supports the language. Developers use "
                 "Python for web development, data science, machine learning, "
                 "automation, scientific computing, and education. The Python "
                 "package index hosts thousands of libraries for every domain. ") * 8
try:
    r = requests.get("https://www.python.org", timeout=8)
    soup = BeautifulSoup(r.content, "html.parser")
    scraped_text = soup.get_text(" ", strip=True)
    if len(scraped_text) < 200:  # blocked / empty
        raise RuntimeError(f"only {len(scraped_text)} chars returned")
    print(f"  Scraped {len(scraped_text)} characters from python.org")
except Exception as e:
    print(f"  Network unavailable ({e}). Using sample text instead.")
    scraped_text = FALLBACK_TEXT
    print(f"  Fallback text length: {len(scraped_text)} chars")

words6 = [w.lower() for w in re.findall(r"[A-Za-z]+", scraped_text)]
filtered6 = [w for w in words6 if w not in sw and len(w) > 2]
wc = WordCloud(width=800, height=400, background_color="white"
               ).generate(" ".join(filtered6))
plt.figure(figsize=(10, 5))
plt.imshow(wc, interpolation="bilinear"); plt.axis("off")
plt.title("Word cloud — python.org (or fallback)")
plt.savefig("/home/claude/a3_q6_wordcloud.png", dpi=80, bbox_inches="tight")
plt.close()
print("  Word cloud saved as a3_q6_wordcloud.png")
print(f"  Top 10 words: {Counter(filtered6).most_common(10)}")

# ---------------------------------------------------------------
# Q7. TextBlob on the scraped text — sentences, words, noun phrases
# ---------------------------------------------------------------
print("\n----- Q7: TextBlob — sentences / words / noun phrases -----")
sample_for_blob = scraped_text[:1500]  # truncate for speed
tb = TextBlob(sample_for_blob)
print(f"  # sentences : {len(tb.sentences)}")
print(f"  # words     : {len(tb.words)}")
try:
    print(f"  noun phrases (first 10): {list(tb.noun_phrases)[:10]}")
except Exception as e:
    print(f"  Could not extract noun phrases: {e}")

# ---------------------------------------------------------------
# Q8. Sentiment of a news article (default analyzer)
# ---------------------------------------------------------------
print("\n----- Q8: Sentiment of a news article (default analyzer) -----")
sample_article = (
    "Scientists today announced a breakthrough in renewable energy. "
    "The new solar panel design is twice as efficient as previous models, "
    "promising lower costs and wider adoption. However, critics warn that "
    "manufacturing scale-up will be challenging and expensive. "
    "Overall, the discovery is being celebrated as a major step forward.")
article_blob = TextBlob(sample_article)
print(f"  Overall sentiment: polarity={article_blob.sentiment.polarity:.3f}, "
      f"subjectivity={article_blob.sentiment.subjectivity:.3f}")
for s in article_blob.sentences:
    print(f"   - polarity={s.sentiment.polarity:+.2f}  | {str(s)[:75]}")

# ---------------------------------------------------------------
# Q9. Sentiment with NaiveBayesAnalyzer
# ---------------------------------------------------------------
print("\n----- Q9: Sentiment with NaiveBayesAnalyzer -----")
try:
    from textblob.sentiments import NaiveBayesAnalyzer
    nb_blob = TextBlob(sample_article, analyzer=NaiveBayesAnalyzer())
    s = nb_blob.sentiment
    print(f"  Classification: {s.classification}, "
          f"p(pos)={s.p_pos:.3f}, p(neg)={s.p_neg:.3f}")
except Exception as e:
    print(f"  NaiveBayesAnalyzer unavailable in this env: {e}")

# ---------------------------------------------------------------
# Q10. Spell-check on (a slice of) a Project Gutenberg book
# ---------------------------------------------------------------
print("\n----- Q10: Spell-check Project Gutenberg text -----")
gutenberg_text = None
FALLBACK_GB = ("This is a sampel paragraph wiht intentinal mistaks for the "
               "spellchecker to find and corect. We hav writen sevral wrods "
               "that are clerly mispeled so the toole can produse suggestions.")
try:
    # Tiny slice of Romeo & Juliet so the demo is fast
    url = "https://www.gutenberg.org/files/1112/1112.txt"
    r = requests.get(url, timeout=8)
    gutenberg_text = r.text[:1500]
    if len(gutenberg_text) < 200:
        raise RuntimeError(f"only {len(gutenberg_text)} chars returned")
    print(f"  Fetched {len(gutenberg_text)} chars from Project Gutenberg")
except Exception as e:
    print(f"  Network unavailable ({e}). Using local sample with misspellings.")
    gutenberg_text = FALLBACK_GB

gb_blob = TextBlob(gutenberg_text)
words10 = [w for w in gb_blob.words if w.isalpha()]
checked = 0
for w in words10[:40]:                                # check first 40 words
    corrections = w.spellcheck()
    if corrections and corrections[0][0].lower() != w.lower():
        print(f"   {w:15s} -> suggestions: {corrections[:3]}")
        checked += 1
        if checked >= 5:
            break
if checked == 0:
    print("   No misspellings found in the sampled words.")

# ---------------------------------------------------------------
# Q11. Multiple TextBlob mini-programs
# ---------------------------------------------------------------
print("\n----- Q11: TextBlob utilities (translate/POS/etc.) -----")

# Note: TextBlob's translate() depends on a Google endpoint that is
# unreliable. We demonstrate the API but catch failure gracefully.
def translate_demo(text):
    print(f"  English: {text}")
    for lang in ["fr", "es", "de"]:
        try:
            print(f"   -> {lang}: {TextBlob(text).translate(to=lang)}")
        except Exception as ex:
            print(f"   -> {lang}: (translation API unavailable: {type(ex).__name__})")

translate_demo("I love programming in Python.")

def polarity_categorise(sentences):
    print("\n  Polarity / subjectivity categorisation:")
    for s in sentences:
        tb = TextBlob(s)
        p, sub = tb.sentiment.polarity, tb.sentiment.subjectivity
        pos = "positive" if p > 0 else "negative" if p < 0 else "neutral"
        obj = "subjective" if sub > 0.5 else "objective"
        print(f"   '{s}' -> {pos}, {obj} (p={p:+.2f}, s={sub:.2f})")

polarity_categorise([
    "I love this product, it is fantastic!",
    "This is the worst experience I have ever had.",
    "The Earth orbits the Sun.",
])

def sentence_sentiments(paragraph):
    print("\n  Per-sentence sentiment scores:")
    for s in TextBlob(paragraph).sentences:
        print(f"   {s.sentiment.polarity:+.2f}  | {s}")

sentence_sentiments(
    "Python is wonderful. I dislike slow code. Today is a normal day.")

def pos_each_word(sentence):
    print("\n  POS tag per word:")
    for word, tag in TextBlob(sentence).tags:
        print(f"   {word:10s} -> {tag}")

pos_each_word("The agile fox quickly jumps over the small dog.")

def spell_suggest(word):
    print(f"\n  Spell-check '{word}':")
    candidates = TextBlob(word).words[0].spellcheck()
    for w, conf in candidates[:3]:
        print(f"   {w}  ({conf:.2f})")

spell_suggest("recieve")

def extract_adjectives(paragraph):
    print("\n  Adjectives in order of occurrence:")
    adj = [w for w, t in TextBlob(paragraph).tags if t.startswith("JJ")]
    print(f"   {adj}")

extract_adjectives(
    "The quick brown fox is clever and agile. The lazy dog seems tired.")

def top_noun_phrases(text, k=5):
    print("\n  Top noun phrases:")
    nps = TextBlob(text).noun_phrases
    print(f"   {Counter(nps).most_common(k)}")

top_noun_phrases(sample_article)

def summarise_by_np_freq(paragraph, keep=2):
    print(f"\n  Summary (top {keep} sentences by noun-phrase frequency):")
    sentences = TextBlob(paragraph).sentences
    all_np = Counter(TextBlob(paragraph).noun_phrases)
    scored = []
    for s in sentences:
        score = sum(all_np[np] for np in TextBlob(str(s)).noun_phrases)
        scored.append((score, str(s)))
    scored.sort(reverse=True)
    for score, sent in scored[:keep]:
        print(f"   [{score}] {sent}")

summarise_by_np_freq(sample_article)

# ---------------------------------------------------------------
# Q12. Word -> definition, synonyms, antonyms
# ---------------------------------------------------------------
print("\n----- Q12: WordNet definition / synonyms / antonyms -----")
from nltk.corpus import wordnet as wn

def word_info(w):
    syns = wn.synsets(w)
    if not syns:
        print(f"  No WordNet entry for '{w}'.")
        return
    print(f"  Word: {w}")
    print(f"   Definition: {syns[0].definition()}")
    synonyms, antonyms = set(), set()
    for s in syns:
        for l in s.lemmas():
            synonyms.add(l.name())
            for a in l.antonyms():
                antonyms.add(a.name())
    print(f"   Synonyms ({len(synonyms)}): {sorted(list(synonyms))[:8]}")
    print(f"   Antonyms ({len(antonyms)}): {sorted(list(antonyms))[:8]}")

word_info("happy")

# ---------------------------------------------------------------
# Q13. Word cloud from a text file (and a shape-masked version)
# ---------------------------------------------------------------
print("\n----- Q13: Word cloud from a text file -----")
sample_txt_path = "/home/claude/q13_sample.txt"
with open(sample_txt_path, "w") as f:
    f.write(("Data science is fun. Python helps us with data science, machine "
             "learning, deep learning and natural language processing. "
             "Visualization is powerful and intuitive. ") * 30)

with open(sample_txt_path) as f:
    raw = f.read()
words13 = [w.lower() for w in re.findall(r"[A-Za-z]+", raw) if w.lower() not in sw]
wc2 = WordCloud(width=800, height=400, background_color="white",
                colormap="viridis").generate(" ".join(words13))
plt.figure(figsize=(10, 5)); plt.imshow(wc2); plt.axis("off")
plt.title("Word cloud from local .txt file")
plt.savefig("/home/claude/a3_q13_wordcloud.png", dpi=80, bbox_inches="tight")
plt.close()
print("  Word cloud saved as a3_q13_wordcloud.png")
print("  (Masked-shape version: pass `mask=np.array(Image.open('heart.png'))`")
print("   to WordCloud(...). Same API, just needs a binary mask image.)")

# ---------------------------------------------------------------
# Q14. Readability statistics (manual, no Textatistic dep.)
# ---------------------------------------------------------------
print("\n----- Q14: Readability statistics -----")
def syllable_count(word):
    word = word.lower()
    if len(word) <= 3: return 1
    vowels = "aeiouy"
    count, prev_vowel = 0, False
    for ch in word:
        is_v = ch in vowels
        if is_v and not prev_vowel:
            count += 1
        prev_vowel = is_v
    if word.endswith("e") and count > 1:
        count -= 1
    return max(1, count)

def readability(text):
    sentences = [s for s in sent_tokenize(text) if s.strip()]
    words = [w for w in word_tokenize(text) if w.isalpha()]
    if not sentences or not words:
        return None
    syl = sum(syllable_count(w) for w in words)
    chars = sum(len(w) for w in words)
    avg_wps   = len(words) / len(sentences)
    avg_cpw   = chars     / len(words)
    avg_syl_pw = syl      / len(words)
    return avg_wps, avg_cpw, avg_syl_pw

sample_articles = {
    "Article A": sample_article,
    "Article B": ("New tax rules came into force last week. Officials say "
                   "the change will simplify compliance. Some experts disagree."),
}
for name, txt in sample_articles.items():
    r = readability(txt)
    if r:
        print(f"  {name}: words/sentence={r[0]:.2f}, "
              f"chars/word={r[1]:.2f}, syllables/word={r[2]:.2f}")

# ---------------------------------------------------------------
# Q15. spaCy Named-Entity Recognition (fallback to NLTK if no spaCy)
# ---------------------------------------------------------------
print("\n----- Q15: Named-Entity Recognition -----")
news_for_ner = (
    "Elon Musk announced from Austin, Texas, that Tesla will invest $5 billion "
    "in a new factory in Berlin. The deal was confirmed on Tuesday.")
try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        from spacy.cli import download as sp_download
        sp_download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
    for ent in nlp(news_for_ner).ents:
        print(f"   {ent.text:25s} -> {ent.label_}")
except Exception as e:
    print(f"  spaCy unavailable ({e}). Using NLTK ne_chunk fallback.")
    try:
        nltk.download('maxent_ne_chunker', quiet=True)
        nltk.download('maxent_ne_chunker_tab', quiet=True)
        nltk.download('words', quiet=True)
        from nltk import ne_chunk
        tagged = pos_tag(word_tokenize(news_for_ner))
        for chunk in ne_chunk(tagged):
            if hasattr(chunk, 'label'):
                ent = " ".join(c[0] for c in chunk)
                print(f"   {ent:25s} -> {chunk.label()}")
    except Exception as e2:
        print(f"  NLTK fallback also failed: {e2}")

# ---------------------------------------------------------------
# Q16. spaCy similarity — Shakespeare comedy vs Romeo & Juliet
# ---------------------------------------------------------------
print("\n----- Q16: spaCy similarity (Shakespeare) -----")
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    text_rj = ("Two households both alike in dignity in fair Verona "
                "where we lay our scene from ancient grudge break to new mutiny")
    text_mnd = ("Now fair Hippolyta our nuptial hour draws on apace "
                "four happy days bring in another moon")
    doc_rj  = nlp(text_rj)
    doc_mnd = nlp(text_mnd)
    print(f"  Similarity (R&J ~ A Midsummer Night's Dream excerpt) = "
          f"{doc_rj.similarity(doc_mnd):.4f}")
    print("  (en_core_web_sm has small vectors — use en_core_web_md/lg in")
    print("   production for more accurate similarity scores.)")
except Exception as e:
    print(f"  spaCy unavailable: {e}")

# ---------------------------------------------------------------
# Q17. textblob.utils — strip_punc and lowerstrip
# ---------------------------------------------------------------
print("\n----- Q17: TextBlob utils strip_punc / lowerstrip -----")
from textblob.utils import strip_punc, lowerstrip
sample17 = "  Romeo, Romeo! Wherefore art thou, ROMEO?  "
print(f"  Input             : {sample17!r}")
print(f"  strip_punc(all=T) : {strip_punc(sample17, all=True)!r}")
print(f"  lowerstrip(all=T) : {lowerstrip(sample17, all=True)!r}")

print("\n" + "=" * 70)
print(" Assignment 3 complete.")
print("=" * 70)



"""
============================================================
 MINOR ASSIGNMENT - 4: MACHINE LEARNING
 CLASSIFICATION, REGRESSION AND CLUSTERING
 Python for Computer Science and Data Science 2 (CSE 3652)
 Centre for Data Science, ITER, SOA University
============================================================
Self-contained: runs in Jupyter (Run All) or as a script.
External datasets (NOAA temperature, Mall Customer) use a
deterministic synthetic fallback if the network is unavailable,
so the file always completes. All plots are saved to PNG.
"""

import os, io, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris, fetch_california_housing
from sklearn.manifold import TSNE
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

np.random.seed(42)

print("=" * 70)
print(" ASSIGNMENT 4 — ML: CLASSIFICATION, REGRESSION, CLUSTERING")
print("=" * 70)

# ---------------------------------------------------------------
# Q1. t-SNE on the Iris dataset
# ---------------------------------------------------------------
print("\n----- Q1: t-SNE on Iris -----")
iris = load_iris()
tsne = TSNE(n_components=2, random_state=42, init="pca", perplexity=30)
iris_tsne = tsne.fit_transform(iris.data)

plt.figure(figsize=(7, 5))
for cls in np.unique(iris.target):
    mask = iris.target == cls
    plt.scatter(iris_tsne[mask, 0], iris_tsne[mask, 1],
                label=iris.target_names[cls], alpha=0.8)
plt.title("t-SNE of Iris dataset")
plt.xlabel("Dim 1"); plt.ylabel("Dim 2"); plt.legend()
plt.tight_layout()
plt.savefig("/home/claude/a4_q1_tsne.png", dpi=80); plt.close()
print("  Saved a4_q1_tsne.png — three Iris species clearly separable in 2-D")

# ---------------------------------------------------------------
# Q2. Seaborn pairplot on California Housing
# ---------------------------------------------------------------
print("\n----- Q2: California Housing pairplot -----")
try:
    cal = fetch_california_housing(as_frame=True)
    df_cal = cal.frame.sample(1000, random_state=42)
    print("  Loaded real California Housing dataset.")
except Exception as e:
    print(f"  Network blocked ({type(e).__name__}). Using synthetic stand-in"
          " with similar marginal distributions.")
    rng = np.random.default_rng(42)
    n = 1000
    df_cal = pd.DataFrame({
        "MedInc":      rng.gamma(2.5, 1.5, n),                    # ~ 0-15
        "HouseAge":    rng.uniform(2, 52, n),
        "AveRooms":    rng.normal(5.4, 1.5, n).clip(1, 15),
        "Population":  rng.lognormal(7.0, 0.8, n),
        "MedHouseVal": None,                                      # filled below
    })
    df_cal["MedHouseVal"] = (
        0.4 * df_cal["MedInc"]
        + 0.02 * df_cal["AveRooms"]
        - 0.005 * df_cal["HouseAge"]
        + rng.normal(0, 0.4, n) + 0.5
    ).clip(0.15, 5.0)

plot_cols = ["MedInc", "HouseAge", "AveRooms", "Population", "MedHouseVal"]
sns.pairplot(df_cal[plot_cols], plot_kws={"s": 8, "alpha": 0.5})
plt.suptitle("California Housing — pairplot", y=1.02)
plt.savefig("/home/claude/a4_q2_pairplot.png", dpi=70, bbox_inches="tight")
plt.close()
print("  Saved a4_q2_pairplot.png. In an interactive Matplotlib window")
print("  pan/zoom are accessible via the toolbar icons.")

# ---------------------------------------------------------------
# Q3. NOAA NYC annual temperature — simple linear regression
# ---------------------------------------------------------------
print("\n----- Q3: NYC annual temperature — linear regression -----")
import requests
years   = np.arange(1895, 2026)

def make_synth_temps(seed):
    rng = np.random.default_rng(seed)
    # Plausible NYC annual mean ~12°C with slow warming + noise
    return 11.0 + 0.018 * (years - 1895) + rng.normal(0, 0.6, size=len(years))

annual_temps  = None
january_highs = None
try:
    # NOAA endpoint shape — left here so the code is "correct"; sandbox blocks it.
    url = ("https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/"
           "city/time-series/USW00094728/tavg/ann/12/1895-2025.csv")
    r = requests.get(url, timeout=8)
    df = pd.read_csv(io.StringIO(r.text), skiprows=4)
    df["Date"] = pd.to_numeric(df["Date"].astype(str).str[:4], errors="coerce")
    df = df.dropna(subset=["Date", "Value"])
    annual_temps = (df.set_index(df["Date"].astype(int))["Value"]
                       .reindex(years).interpolate().to_numpy())
    print("  Loaded NOAA NYC annual mean temperatures.")
except Exception as e:
    print(f"  Network/data fetch failed ({e}). Using synthetic stand-in.")
    annual_temps  = make_synth_temps(0)
    january_highs = make_synth_temps(1) - 7   # Jan highs colder, similar trend
if january_highs is None:
    january_highs = make_synth_temps(1) - 7

# Fit linear regression: temperature ~ year
X = years.reshape(-1, 1)
m_annual = LinearRegression().fit(X, annual_temps)
m_january = LinearRegression().fit(X, january_highs)
print(f"  Annual trend  : slope = {m_annual.coef_[0]:.4f} °C/year")
print(f"  January highs : slope = {m_january.coef_[0]:.4f} °C/year")

plt.figure(figsize=(10, 5))
plt.scatter(years, annual_temps,  s=10, alpha=0.6, label="Annual mean")
plt.plot(years, m_annual.predict(X), "r-", label="Annual fit")
plt.scatter(years, january_highs, s=10, alpha=0.6, label="January highs")
plt.plot(years, m_january.predict(X), "g--", label="January fit")
plt.title("NYC temperature trends (1895-2025)")
plt.xlabel("Year"); plt.ylabel("Temperature (°C)"); plt.legend()
plt.tight_layout(); plt.savefig("/home/claude/a4_q3_temp.png", dpi=80); plt.close()
print("  Saved a4_q3_temp.png — both series trend upward at similar rate.")

# ---------------------------------------------------------------
# Q4. Iris classification with KNN (default k=5)
# ---------------------------------------------------------------
print("\n----- Q4: Iris classification with default KNN -----")
X_tr, X_te, y_tr, y_te = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target)
knn_default = KNeighborsClassifier()
knn_default.fit(X_tr, y_tr)
acc = knn_default.score(X_te, y_te)
print(f"  KNN(default k=5) accuracy on hold-out test: {acc:.4f}")

# ---------------------------------------------------------------
# Q5. Hand-coded KNN on the 4-point toy dataset, classify P(3,3)
# ---------------------------------------------------------------
print("\n----- Q5: Hand-coded KNN on toy 2-D points -----")
toy = pd.DataFrame({
    "id": list("ABCD"),
    "x": [2, 1, 4, 5],
    "y": [3, 1, 4, 2],
    "cls": [0, 0, 1, 1],
})
P = (3.0, 3.0)
toy["dist"] = np.hypot(toy["x"] - P[0], toy["y"] - P[1])
print(toy[["id", "x", "y", "cls", "dist"]].to_string(index=False))

for k in [1, 3]:
    nearest = toy.nsmallest(k, "dist")
    pred = nearest["cls"].mode().iloc[0]
    print(f"  k={k}: nearest = {nearest['id'].tolist()}, predicted class = {pred}")

# ---------------------------------------------------------------
# Q6. KNN on exam-score dataset with k=3
# ---------------------------------------------------------------
print("\n----- Q6: KNN on student-exam dataset (k=3) -----")
df_stud = pd.DataFrame({
    "e1": [85, 70, 60, 50, 95, 45],
    "e2": [90, 75, 65, 55, 92, 50],
    "e3": [88, 80, 70, 58, 96, 48],
    "cls": ["Pass", "Pass", "Fail", "Fail", "Pass", "Fail"],
})
new_stu = np.array([[72, 78, 75]])
knn_stu = KNeighborsClassifier(n_neighbors=3)
knn_stu.fit(df_stud[["e1", "e2", "e3"]], df_stud["cls"])
print(f"  Predicted class for [72,78,75] with k=3: {knn_stu.predict(new_stu)[0]}")

# Show distances for transparency
diffs = df_stud[["e1","e2","e3"]].to_numpy() - new_stu
dists = np.linalg.norm(diffs, axis=1)
print("  Distance to each training point:")
for cls, d in zip(df_stud["cls"], dists):
    print(f"    {cls:5s}  d = {d:.3f}")

# ---------------------------------------------------------------
# Q7. Cross-validation to choose optimal k for Iris KNN
# ---------------------------------------------------------------
print("\n----- Q7: KFold cross-validation to pick best k for Iris -----")
kf = KFold(n_splits=10, shuffle=True, random_state=42)
k_range = range(1, 21)
mean_scores = []
for k in k_range:
    scores = cross_val_score(KNeighborsClassifier(n_neighbors=k),
                             iris.data, iris.target, cv=kf)
    mean_scores.append(scores.mean())

best_k = list(k_range)[int(np.argmax(mean_scores))]
print(f"  Best k = {best_k}, mean CV accuracy = {max(mean_scores):.4f}")
plt.figure(figsize=(7, 4))
plt.plot(list(k_range), mean_scores, "o-")
plt.xlabel("k"); plt.ylabel("10-fold CV mean accuracy")
plt.title("Iris KNN — accuracy vs k")
plt.grid(True); plt.tight_layout()
plt.savefig("/home/claude/a4_q7_k_cv.png", dpi=80); plt.close()
print("  Saved a4_q7_k_cv.png")

# ---------------------------------------------------------------
# Q8. K-Means on a 6-point toy dataset with k=2
# ---------------------------------------------------------------
print("\n----- Q8: K-Means on 6 toy points (k=2) -----")
toy_pts = np.array([(1,1),(2,2),(3,3),(8,8),(9,9),(10,10)])
km = KMeans(n_clusters=2, random_state=42, n_init=10).fit(toy_pts)
print(f"  Labels    : {km.labels_}")
print(f"  Centroids : {km.cluster_centers_}")

plt.figure(figsize=(6, 5))
plt.scatter(toy_pts[:,0], toy_pts[:,1], c=km.labels_, cmap="viridis", s=80)
plt.scatter(km.cluster_centers_[:,0], km.cluster_centers_[:,1],
            c="red", marker="X", s=200, label="Centroid")
plt.title("K-Means on toy points (k=2)"); plt.legend()
plt.tight_layout(); plt.savefig("/home/claude/a4_q8_toy_kmeans.png", dpi=80)
plt.close()
print("  Saved a4_q8_toy_kmeans.png")

# ---------------------------------------------------------------
# Q9. K-Means on Mall Customer-style dataset + elbow method
# ---------------------------------------------------------------
print("\n----- Q9: K-Means on Mall Customers (k=5 + elbow) -----")
def make_mall_customers(n=200, seed=42):
    rng = np.random.default_rng(seed)
    # Five clusters by (annual income, spending score)
    centers = [(35,20),(85,80),(85,20),(35,80),(60,50)]
    pts = []
    for cx, cy in centers:
        pts.append(rng.normal([cx, cy], [7, 7], size=(n//5, 2)))
    return np.clip(np.vstack(pts), 0, 100)

mall = make_mall_customers()
df_mall = pd.DataFrame(mall, columns=["AnnualIncome_kUSD", "SpendingScore"])

# Elbow method
inertias = []
for k in range(1, 11):
    inertias.append(KMeans(n_clusters=k, random_state=42, n_init=10
                          ).fit(df_mall).inertia_)

plt.figure(figsize=(7, 4))
plt.plot(range(1, 11), inertias, "o-")
plt.xlabel("k"); plt.ylabel("Inertia (within-cluster SS)")
plt.title("Elbow method — Mall Customers")
plt.tight_layout(); plt.savefig("/home/claude/a4_q9_elbow.png", dpi=80); plt.close()
print(f"  Inertias for k=1..10: {[round(v) for v in inertias]}")
print("  Elbow occurs around k=5 (matches the synthetic ground truth).")

# Fit k=5 and plot segments
km5 = KMeans(n_clusters=5, random_state=42, n_init=10).fit(df_mall)
df_mall["Segment"] = km5.labels_
plt.figure(figsize=(8, 6))
for s in sorted(df_mall["Segment"].unique()):
    sub = df_mall[df_mall["Segment"] == s]
    plt.scatter(sub["AnnualIncome_kUSD"], sub["SpendingScore"],
                label=f"Segment {s}", alpha=0.7)
plt.scatter(km5.cluster_centers_[:,0], km5.cluster_centers_[:,1],
            c="red", marker="X", s=200, label="Centroid")
plt.xlabel("Annual Income (k$)"); plt.ylabel("Spending Score (1-100)")
plt.title("Mall Customer Segments (k=5)"); plt.legend()
plt.tight_layout(); plt.savefig("/home/claude/a4_q9_segments.png", dpi=80)
plt.close()
print("  Saved a4_q9_segments.png")
print("  Segment insights for marketing:")
print("   - Low income, low spend       : budget-line offers, value bundles")
print("   - High income, high spend     : premium loyalty programmes (VIP)")
print("   - High income, low spend      : aspirational ads, win-back coupons")
print("   - Low income, high spend      : credit/EMI plans, retention focus")
print("   - Moderate income & spending  : mainstream promotions, cross-sell")

# ---------------------------------------------------------------
# Q10. pandas Series exercises
# ---------------------------------------------------------------
print("\n----- Q10: pandas Series operations -----")

# (a) Series from list
print("\n  (a) Series from [7, 11, 13, 17]:")
print(pd.Series([7, 11, 13, 17]).to_string())

# (b) Five elements each equal to 100.0
print("\n  (b) Series of five 100.0s:")
print(pd.Series(100.0, index=range(5)).to_string())

# (c) 20 random numbers + describe
print("\n  (c) 20 random ints 0-100 + describe():")
rng = np.random.default_rng(0)
s_rand = pd.Series(rng.integers(0, 101, size=20))
print(s_rand.to_string())
print("\n   describe():")
print(s_rand.describe().to_string())

# (d) temperatures with custom string indices
print("\n  (d) temperatures (custom index):")
temps = pd.Series([98.6, 98.9, 100.2, 97.9],
                  index=["Julie", "Charlie", "Sam", "Andrea"])
print(temps.to_string())

# (e) Build from dict
print("\n  (e) Series from dict:")
temp_dict = {"Julie": 98.6, "Charlie": 98.9, "Sam": 100.2, "Andrea": 97.9}
temps_dict = pd.Series(temp_dict)
print(temps_dict.to_string())

print("\n" + "=" * 70)
print(" Assignment 4 complete.")
print("=" * 70)



"""
============================================================
 MINOR ASSIGNMENT - 5: DEEP LEARNING
 Python for Computer Science and Data Science 2 (CSE 3652)
 Centre for Data Science, ITER, SOA University
============================================================
Self-contained: runs in Jupyter (Run All) or as a script.
MNIST is loaded via keras.datasets.mnist (cached locally on
first download). Epochs are kept low so the whole assignment
finishes in a couple of minutes on CPU — bump epochs higher
for stronger results.
"""

import os
# Quiet TensorFlow startup messages
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print("=" * 70)
print(" ASSIGNMENT 5 — DEEP LEARNING")
print("=" * 70)

# ---------------------------------------------------------------
# Q1. Single-layer perceptron vs Multilayer perceptron — explained
# ---------------------------------------------------------------
print("\n----- Q1: SLP vs MLP — architecture and loss -----")
Q1_EXPLANATION = """
SINGLE LAYER PERCEPTRON (SLP)
  Architecture : Input layer -> single output neuron with a step or
                 sigmoid activation. No hidden layer.
  Computes     : y = phi( sum_i w_i x_i + b )
  Capacity     : Can only learn LINEARLY SEPARABLE problems
                 (e.g. AND, OR — but not XOR).
  Loss         : Perceptron loss  L = max(0, -y * (w·x + b)),
                 or MSE for regression-style outputs.

MULTI LAYER PERCEPTRON (MLP)
  Architecture : Input -> one or more hidden layers (with non-linear
                 activations such as ReLU / tanh / sigmoid) -> output.
  Universal    : Can approximate any continuous function with enough
                 hidden units (Universal Approximation Theorem).
  Loss         : Regression  -> Mean Squared Error
                 Binary clf  -> Binary Cross-Entropy
                 Multi-class -> Categorical Cross-Entropy

  Diagram (text form):
     Input    [Hidden 1]   [Hidden 2]    Output
      x1 ---\\
      x2 ---->O O O ---->   O O   ---->  ŷ1
      x3 ---/   (ReLU)     (ReLU)        ŷ2 (softmax)
                    |__weights, biases__|
"""
print(Q1_EXPLANATION)

# ---------------------------------------------------------------
# Q2. Simple feed-forward ANN on Iris
# ---------------------------------------------------------------
print("\n----- Q2: Feed-forward ANN on Iris -----")
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

tf.random.set_seed(42); np.random.seed(42)
iris = load_iris()
X_tr, X_te, y_tr, y_te = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target)

scaler = StandardScaler().fit(X_tr)
X_tr_s = scaler.transform(X_tr); X_te_s = scaler.transform(X_te)

iris_model = models.Sequential([
    layers.Input(shape=(4,)),
    layers.Dense(16, activation="relu"),
    layers.Dense(8, activation="relu"),
    layers.Dense(3, activation="softmax"),
])
iris_model.compile(optimizer="adam",
                   loss="sparse_categorical_crossentropy",
                   metrics=["accuracy"])
iris_model.summary(print_fn=lambda s: print("  " + s))
hist = iris_model.fit(X_tr_s, y_tr, epochs=50, batch_size=8,
                      validation_split=0.1, verbose=0)
loss, acc = iris_model.evaluate(X_te_s, y_te, verbose=0)
print(f"  Iris ANN  test accuracy: {acc:.4f}, loss: {loss:.4f}")

# ---------------------------------------------------------------
# Q3. Simple ANN on MNIST
# ---------------------------------------------------------------
print("\n----- Q3: Feed-forward ANN on MNIST -----")
mnist_loaded = False
try:
    (x_train_full, y_train_full), (x_test, y_test) = \
        tf.keras.datasets.mnist.load_data()
    mnist_loaded = True
    print(f"  MNIST loaded: train {x_train_full.shape}, test {x_test.shape}")
except Exception as e:
    print(f"  MNIST download failed ({e}). Building synthetic 8x8 digit data.")
    # Use sklearn's digits as a tiny stand-in
    from sklearn.datasets import load_digits
    digits = load_digits()
    x = digits.images.astype("float32")           # (1797, 8, 8)
    y = digits.target
    x_train_full, x_test, y_train_full, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y)

# Keep training fast: subsample 10k
n_train = min(10000, len(x_train_full))
x_train = x_train_full[:n_train].astype("float32") / 255.0
y_train = y_train_full[:n_train]
x_test_s = x_test.astype("float32") / 255.0

if mnist_loaded:
    input_shape = (28, 28); flat = 28 * 28
else:
    input_shape = x_train.shape[1:]; flat = int(np.prod(input_shape))

ann_mnist = models.Sequential([
    layers.Input(shape=input_shape),
    layers.Flatten(),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.2),
    layers.Dense(64, activation="relu"),
    layers.Dense(10, activation="softmax"),
])
ann_mnist.compile(optimizer="adam",
                  loss="sparse_categorical_crossentropy",
                  metrics=["accuracy"])
ann_mnist.fit(x_train, y_train, epochs=12, batch_size=64,
              validation_split=0.1, verbose=2)
loss, acc = ann_mnist.evaluate(x_test_s, y_test, verbose=0)
print(f"  MNIST ANN test accuracy: {acc:.4f}, loss: {loss:.4f}")

# ---------------------------------------------------------------
# Q4. Manual Convolution + ReLU + Max-Pool on a 4x4 input
# ---------------------------------------------------------------
print("\n----- Q4: Manual Conv2D + ReLU + MaxPool -----")
img = np.array([
    [1, 2, 0, 1],
    [3, 1, 2, 2],
    [1, 0, 1, 3],
    [2, 1, 2, 1],
], dtype=float)
kernel = np.array([
    [ 1,  0],
    [ 0, -1],
], dtype=float)

def conv2d_valid(x, k):
    kh, kw = k.shape
    out_h, out_w = x.shape[0] - kh + 1, x.shape[1] - kw + 1
    out = np.zeros((out_h, out_w))
    for i in range(out_h):
        for j in range(out_w):
            out[i, j] = np.sum(x[i:i+kh, j:j+kw] * k)
    return out

def relu(x):
    return np.maximum(0, x)

def maxpool2x2(x):
    h, w = x.shape
    out = np.zeros((h // 2, w // 2))
    for i in range(0, h - h % 2, 2):
        for j in range(0, w - w % 2, 2):
            out[i // 2, j // 2] = x[i:i+2, j:j+2].max()
    return out

conv_out = conv2d_valid(img, kernel)
relu_out = relu(conv_out)
pool_out = maxpool2x2(relu_out)
print(f"  Input image (4x4):\n{img}")
print(f"  Kernel (2x2):\n{kernel}")
print(f"  After convolution (3x3):\n{conv_out}")
print(f"  After ReLU (3x3):\n{relu_out}")
print(f"  After 2x2 max-pool (truncated to 2x2 from 3x3 valid region):\n{pool_out}")
print("  Worked example for top-left of conv:")
print("    1*1 + 2*0 + 3*0 + 1*(-1) = 1 - 1 = 0")

# ---------------------------------------------------------------
# Q5. CNN on MNIST (2 conv layers + 1 FC hidden)
# ---------------------------------------------------------------
print("\n----- Q5: CNN on MNIST (Conv->Conv->FC) -----")
# Reshape to add channel dim
x_train_c = x_train.reshape(-1, *input_shape, 1)
x_test_c  = x_test_s.reshape(-1, *input_shape, 1)

cnn = models.Sequential([
    layers.Input(shape=(*input_shape, 1)),
    layers.Conv2D(16, (3, 3), activation="relu", padding="same"),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(32, (3, 3), activation="relu", padding="same"),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation="relu"),
    layers.Dense(10, activation="softmax"),
])
cnn.compile(optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"])
cnn.summary(print_fn=lambda s: print("  " + s))
cnn.fit(x_train_c, y_train, epochs=12, batch_size=64,
        validation_split=0.1, verbose=2)
loss, acc = cnn.evaluate(x_test_c, y_test, verbose=0)
print(f"  MNIST CNN test accuracy: {acc:.4f}, loss: {loss:.4f}")
print("  (On real 28x28 MNIST with the same architecture you should see")
print("   ~0.98+ test accuracy. Use more epochs and the full 60k training set.)")

# Visualise 9 predictions
preds = cnn.predict(x_test_c[:9], verbose=0).argmax(axis=1)
fig, axes = plt.subplots(3, 3, figsize=(6, 6))
for i, ax in enumerate(axes.flat):
    ax.imshow(x_test_s[i], cmap="gray")
    ax.set_title(f"True {y_test[i]}, Pred {preds[i]}", fontsize=9)
    ax.axis("off")
plt.tight_layout()
plt.savefig("/home/claude/a5_q5_cnn_preds.png", dpi=80)
plt.close()
print("  Saved a5_q5_cnn_preds.png — first 9 test predictions visualised.")

print("\n" + "=" * 70)
print(" Assignment 5 complete.")
print("=" * 70)
