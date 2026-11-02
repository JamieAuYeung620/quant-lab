# %%
d = {}
d['a'] = 1
d['b'] = 2
print(d)
d['a']
d.get('z',0)
print('a' in d)
print('z' in d)

# %%
counts = {}
for ch in "hello":
    counts[ch] = counts.get(ch,0) + 1
counts

counts2 = {}
for ch2 in "olleh":
    counts2[ch2] = counts2.get(ch2,0) + 1
counts2

counts == counts2

# %%
nums = [5, 3, 8, 1]
print(nums[0])
print(nums[-1])
print(nums[1:3])
print(len(nums))
sorted(nums)
# %%
s = "trading"
print(s[0])
print(sorted(s))
# %%
seen = set()
seen.add(3)
seen.add(3)
seen
# %%
