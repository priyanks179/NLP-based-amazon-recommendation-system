import itertools


def remove_dup1(data):
    indices = []
    data_sorted = data[data['title'].apply(lambda x: len(x.split())>4)]# Remove All products with very few words in title
    data_sorted.sort_values('title',inplace=True, ascending=False)#this will sort
    for i,row in data_sorted.iterrows():#give row indices here i gives indices
        indices.append(i)

    stage1_dedupe_asins = []#carry indices to save
    i = 0
    j = 0
    num_data_points = data_sorted.shape[0]
    while i < num_data_points and j < num_data_points:
        
        previous_i = i

        # store the list of words of ith string in a, ex: a = ['tokidoki', 'The', 'Queen', 'of', 'Diamonds', 'Women's', 'Shirt', 'X-Large']
        a = data['title'].loc[indices[i]].split()

        # search for the similar products sequentially 
        j = i+1
        while j < num_data_points:

            # store the list of words of jth string in b, ex: b = ['tokidoki', 'The', 'Queen', 'of', 'Diamonds', 'Women's', 'Shirt', 'Small']
            b = data['title'].loc[indices[j]].split()

            # store the maximum length of two strings
            length = max(len(a), len(b))

            # count is used to store the number of words that are matched in both strings
            count  = 0

            # itertools.zip_longest(a,b): will map the corresponding words in both strings, it will appened None in case of unequal strings
            # example: a =['a', 'b', 'c', 'd']
            # b = ['a', 'b', 'd']
            # itertools.zip_longest(a,b): will give [('a','a'), ('b','b'), ('c','d'), ('d', None)]
            for k in itertools.zip_longest(a,b): 
                if (k[0] == k[1]):
                    count += 1

            # if the number of words in which both strings differ are > 2 , we are considering it as those two apperals are different
            # if the number of words in which both strings differ are < 2 , we are considering it as those two apperals are same, hence we are ignoring them
            if (length - count) > 2: # number of words in which both sensences differ
                # if both strings are differ by more than 2 words we include the 1st string index
                stage1_dedupe_asins.append(data_sorted['asin'].loc[indices[i]])

                # if the comaprision between is between num_data_points, num_data_points-1 strings and they differ in more than 2 words we include both
                if j == num_data_points-1: stage1_dedupe_asins.append(data_sorted['asin'].loc[indices[j]])

                # start searching for similar apperals corresponds 2nd string
                i = j
                break
            else:
                j += 1
        if previous_i == i:
            break
    data = data.loc[data['asin'].isin(stage1_dedupe_asins)]    
    return(data)


def remove_dup2(data):
    indices = []
    for i,row in data.iterrows():
        indices.append(i)

    stage2_dedupe_asins = []
    while len(indices)!=0:
        i = indices.pop()
        stage2_dedupe_asins.append(data['asin'].loc[i])
        # consider the first apperal's title
        a = data['title'].loc[i].split()
        # store the list of words of ith string in a, ex: a = ['tokidoki', 'The', 'Queen', 'of', 'Diamonds', 'Women's', 'Shirt', 'X-Large']
        for j in indices:
            
            b = data['title'].loc[j].split()
            # store the list of words of jth string in b, ex: b = ['tokidoki', 'The', 'Queen', 'of', 'Diamonds', 'Women's', 'Shirt', 'X-Large']
            
            length = max(len(a),len(b))
            
            # count is used to store the number of words that are matched in both strings
            count  = 0

            # itertools.zip_longest(a,b): will map the corresponding words in both strings, it will appened None in case of unequal strings
            # example: a =['a', 'b', 'c', 'd']
            # b = ['a', 'b', 'd']
            # itertools.zip_longest(a,b): will give [('a','a'), ('b','b'), ('c','d'), ('d', None)]
            for k in itertools.zip_longest(a,b): 
                if (k[0]==k[1]):
                    count += 1

            # if the number of words in which both strings differ are < 3 , we are considering it as those two apperals are same, hence we are ignoring them
            if (length - count) < 3:
                indices.remove(j)
    data = data.loc[data['asin'].isin(stage2_dedupe_asins)]
    return(data)
        
