import math
import ElementClass as elm

def SelectionSort(elementContainer):
    elementContainer.sortingMethod = "SelectionSort"
    for i in range(elementContainer.length):
        smallestIndex = i
        for j in range(i+1, elementContainer.length):
            if (elementContainer.CompareToBase(j,smallestIndex,True,1,True,0) > 0):
                smallestIndex = j
        if smallestIndex != i:
            elementContainer.ExchangeElements(i,smallestIndex)
        elementContainer.MarkElement(i,"finish",1)

def BubbleSort(elementContainer):
    elementContainer.sortingMethod = "BubbleSort"
    for i in range(elementContainer.length):
        for j in range(elementContainer.length-i-1):
            if (elementContainer.CompareElements(j,j+1,True,1,True,0) > 0):
                elementContainer.ExchangeElements(j,j+1)
        elementContainer.MarkElement(elementContainer.length-i-1,"finish",1)


def InsertionSort(elementContainer):
    elementContainer.sortingMethod = "InsertionSort"
    for i in range(elementContainer.length):
        elementContainer.MarkElement(i,"processing",0)
        insertIndex = i
        for j in range(i-1,-2,-1):
            if j == -1 or (elementContainer.CompareElements(i,j,True,1,True,0) >= 0):
                insertIndex = j+1
                break
        if insertIndex != i:
            elementContainer.InsertElement(i,insertIndex)
    for i in range(elementContainer.length):
        elementContainer.MarkElement(i,"finish",0)

def QuickSort(elementContainer, l=-1, r=-1):
    if l==-1 and r==-1:
        elementContainer.sortingMethod = "QuickSort"
        l = 0
        r = elementContainer.length - 1
    else:
        elementContainer.CastShader((l,r))
    if l==r:
        elementContainer.MarkElement(l,"finish",1)
        return
    _templ = l+1
    _tempr = r

    while _templ != _tempr:
        while _templ != _tempr and elementContainer.CompareToBase(l,_templ,True,1,True,0) <= 0:
            _templ += 1
        elementContainer.MarkElement(_templ,"smallersign",0)
        while _templ != _tempr and elementContainer.CompareToBase(l,_tempr,True,1,True,0) >= 0:
            _tempr -= 1
        elementContainer.MarkElement(_tempr,"greatersign",1)
        elementContainer.ExchangeElements(_templ, _tempr)

    if elementContainer.CompareToBase(l,_templ,True,1,True,0) >= 0:
        _templ -= 1
    elementContainer.ExchangeElements(l, _templ)
    elementContainer.MarkElement(_templ, "finish", 0)

    if l < _templ-1:
        QuickSort(elementContainer, l, _templ-1)
    else: elementContainer.MarkElement(l,"finish",0)
    if _templ+1 < r:
        QuickSort(elementContainer, _templ+1, r)
    else: elementContainer.MarkElement(r,"finish",0)
    
    if not(l==-1 and r==-1):
        elementContainer.DecastShader()

def MergeSort(elementContainer, l=-1, r=-1):
    if l==-1 and r==-1:
        elementContainer.sortingMethod = "MergeSort"
        l = 0
        r = elementContainer.length - 1
    else:
        elementContainer.CastShader((l,r))
    
    if l == r:
        elementContainer.DecastShader()
        return

    _tempMid = (l + r) // 2

    MergeSort(elementContainer, l, _tempMid)
    MergeSort(elementContainer, _tempMid+1, r)

    _templ = l
    _tempr = _tempMid+1
    _tempL = _tempMid
    _tempR = r

    for i in range(_templ, _tempL+1):
        elementContainer.MarkElement(i,"smallersign",0)
        
    for i in range(_tempr, _tempR+1):
        elementContainer.MarkElement(i,"greatersign",0)

    _tempIndex = l

    while _templ <= _tempL and _tempr <= _tempR:
        elementContainer.MarkElement(_tempIndex,"processing",1)
        if elementContainer.CompareElements(_templ, _tempr, True, 1, True, 0) < 0:
            _templ += 1
        else:
            elementContainer.InsertElement(_tempr, _tempIndex)
            _tempr += 1
            _templ += 1
            _tempL += 1
        _tempIndex += 1
    
    if not(l==-1 and r==-1):
        elementContainer.DecastShader()

def HeapSort(elementContainer):
    elementContainer.sortingMethod = "HeapSort"
    for i in range(elementContainer.length):
        if math.floor(math.log2(i + 1)) % 2 == 0:
            elementContainer.MarkElement(i,"special",0)
        else:
            elementContainer.MarkElement(i,"processing",0)
    for i in range(elementContainer.length // 2 - 1, -1, -1):
        _tempFather = i;
        _tempSon = _tempFather * 2 + 1;
        while _tempSon <= elementContainer.length - 1:
            if _tempSon + 1 <= elementContainer.length - 1 and elementContainer.CompareElements(_tempSon, _tempSon + 1) < 0:
                _tempSon += 1
            if elementContainer.CompareElements(_tempFather, _tempSon) > 0:
                break
            else:
                elementContainer.ExchangeElements(_tempFather, _tempSon)

                if math.floor(math.log2(_tempFather + 1)) % 2 == 0:
                    elementContainer.MarkElement(_tempFather,"special",0)
                else:
                    elementContainer.MarkElement(_tempFather,"processing",0)
                    
                if math.floor(math.log2(_tempSon + 1)) % 2 == 0:
                    elementContainer.MarkElement(_tempSon,"special",0)
                else:
                    elementContainer.MarkElement(_tempSon,"processing",0)

                _tempFather = _tempSon
                _tempSon = _tempFather * 2 + 1
    for i in range(elementContainer.length - 1, -1, -1): 
        elementContainer.ExchangeElements(0, i)
        elementContainer.MarkElement(0,"special", 0)
        elementContainer.MarkElement(i, "finish", 1)
        _tempFather = 0
        _tempSon = _tempFather * 2 + 1;
        while _tempSon <= i - 1:
            if _tempSon + 1 <= i - 1 and elementContainer.CompareElements(_tempSon, _tempSon + 1) < 0:
                _tempSon += 1
            if elementContainer.CompareElements(_tempFather, _tempSon) > 0:
                break
            else:
                elementContainer.ExchangeElements(_tempFather, _tempSon)
                
                if math.floor(math.log2(_tempFather + 1)) % 2 == 0:
                    elementContainer.MarkElement(_tempFather,"special",0)
                else:
                    elementContainer.MarkElement(_tempFather,"processing",0)
                    
                if math.floor(math.log2(_tempSon + 1)) % 2 == 0:
                    elementContainer.MarkElement(_tempSon,"special",0)
                else:
                    elementContainer.MarkElement(_tempSon,"processing",0)

                _tempFather = _tempSon
                _tempSon = _tempFather * 2 + 1

def RadixSort(elementContainer, radix=4):
    elementContainer.sortingMethod = "RadixSort"
    _maxDigit = 0
    for i in range(elementContainer.length):
        while elementContainer.GetElement(i).value >= (radix ** _maxDigit):
            _maxDigit += 1
    for d in range(_maxDigit):
        radixIndex = [0 for i in range(radix)]
        for i in range(elementContainer.length):
            elementContainer.MarkElement(i,"processing",1)
            elementContainer.MarkElement(i,"unsolved",0)
            _tempDigit = elementContainer.GetElement(i).value // (radix ** d) % radix
            elementContainer.InsertElement(i,radixIndex[_tempDigit])
            for j in range(_tempDigit,radix):
                radixIndex[j] += 1
    for i in range(elementContainer.length):
        elementContainer.MarkElement(i,"finish",0)