package main

import "sort"

func sortReverseSuffixArrayNaive(info *NaiveStruct) {
	reverseSA := info.stringReverseSA

	var reverseIndexSa []int
	oldArray := make([]string, len(reverseSA))
	copy(oldArray, reverseSA)

	sort.Strings(reverseSA)
	for s := range reverseSA {
		reverseIndexSa = append(reverseIndexSa, IndexOf(reverseSA[s], oldArray))
	}

	info.reverseSA = reverseIndexSa
}

func sortSuffixArrayNaive(info *NaiveStruct) {
	SA := info.stringSA

	var indexSa []int
	var oldArray = make([]string, len(SA))
	copy(oldArray, SA)

	sort.Strings(SA)
	for s := range SA {
		indexSa = append(indexSa, IndexOf(SA[s], oldArray))
	}

	info.SA = indexSa

}

func createReverseSuffixArrayNaive(info *NaiveStruct) {

	reverseInput := info.reverseInput

	length := len(reverseInput)
	var reverseSuffixArray []string
	var reverseSuffix string

	for i := 0; i < length; i++ {

		if i != 0 {
			reverseSuffix = reverseSuffix + string(reverseInput[i-1])
		}

		slicePiece := reverseInput[i:length] + reverseSuffix

		reverseSuffixArray = append(reverseSuffixArray, slicePiece)

	}

	info.stringReverseSA = reverseSuffixArray

}

func createSuffixArrayNaive(info *NaiveStruct) {
	input := info.input
	length := len(input)

	var suffixArray []string
	var suffix string

	for i := 0; i < length; i++ {

		if i != 0 {
			suffix = suffix + string(input[i-1])
		}

		slicePiece := input[i:length] + suffix

		suffixArray = append(suffixArray, slicePiece)

	}

	info.stringSA = suffixArray

}

func findBWT(array []string) []string {
	length := len(array)
	var bwt []string
	for _, s := range array {
		bwt = append(bwt, string(s[length-1]))
	}

	return bwt
}

func naiveExactSearch(info *NaiveStruct) int {
	counter := 0
	var indices []int
	k := info.key
	n := info.input

	for i := range n {
		if n[i] == k[0] {
			for j := range k {
				if k[j] == n[i+j] && len(k)+i < len(n) {
					if j+1 == len(k) {
						counter += 1
						indices = append(indices, i)
					}
				} else {
					break
				}

			}
		}

	}
	return counter
}

func naiveApproxSearch(info *NaiveStruct) []int {
	var match []int
	for i := 0; i < len(info.input)-len(info.key); i++ {
		hammingDistance := 0
		for j := i; j < i+len(info.key); j++ {
			if info.input[j] != info.key[j-i] {
				hammingDistance += 1
				if hammingDistance > info.thresHold {
					break
				}
			}
			if j == (i + len(info.key) - 1) {
				match = append(match, i)
			}
		}
	}
	return match
}
