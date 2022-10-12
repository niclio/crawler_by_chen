def combination(A, k):
	chooses = []
	c(A, len(A), k, chooses, k)

def c(A, n, k, chooses, kc):
	# print('chooses=', chooses, 'k=', k)
	if len(chooses)==kc:
		print(chooses)
		return
	if n <= 0: return
	c(A,n-1,k,chooses,kc) # C(n-1,k)

	chooses.append(A[n-1])
	c(A,n-1,k-1,chooses,kc) # C(n-1,k-1)
	del chooses[-1]

combination([1,2,3,4,5], 3)
