def rev(list, stack):			
    if not list:
        return stack
    else: 
        return rev(list[1:], list[:1] + stack)		

def reverse(list):  return rev(list, list[:0])
