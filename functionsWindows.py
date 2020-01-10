# Name: Simar Bhamra
# Student ID: 6364665

import re
import Population
import random
import math
import os

generations = 100
crossover_rate = None
mutation_rate = None
b_size = 1
r = None
# f = None
global_best = [None] * b_size
global_worse = None
initialPOP = None
newPop = None


def geneticAlgo(key_size, cipher, comp, file, crossovertype):
    global initialPOP
    global newPop
    global r
    # global f
    initialPOP = Population.population(key_size, 0)

    for i in range(len(initialPOP)):
        fitscore = fitness(initialPOP[i].chromo, cipher)
        initialPOP[i].value = fitscore

    file.write("Crossover Rate: " + str(crossover_rate) + "\n")
    file.write("Mutation Rate: " + str(mutation_rate) + "\n")
    file.write("Population Size " + str(len(initialPOP)) + "\n")
    file.write("Number of Generations " + str(generations) + "\n")
    file.write("Cipher Text: " + str(cipher) + "\n")
    file.write("CROSSOVER: " + str(crossovertype) + "\n")
    file.write("MUTATION: " + "Inversion Mutation" + "\n")
    file.write("Seed " + str(r) + "\n")
    file.write("\n")

    for i in range(generations):
        # f = open(".\Output\Generation", "a+")
        avgfitness = 0

        initialPOP.sort(key=lambda x: x.value, reverse=False)

        global global_best
        for i in range(len(global_best)):
            global_best[i] = initialPOP[i]

        newPop = Population.population(key_size, 0)
        newPop_size = 0
        i = 0
        while newPop_size < len(initialPOP):
            compititor1 = tournament_selection(initialPOP, comp)
            compititor2 = tournament_selection(initialPOP, comp)
            if (round(random.random(), 2) * 100) < crossover_rate:
                if crossovertype == "1-Point Crossover":
                    compititor1, compititor2 = crossover1point(compititor1.chromo, compititor2.chromo)
                elif crossovertype == "Uniform Crossover":
                    compititor1, compititor2 = uniformcrossover(compititor1.chromo, compititor2.chromo)
                elif crossovertype == "MixNMatch Crossover":
                    compititor1, compititor2 = MixNmatchCrossover(compititor1.chromo, compititor2.chromo)
            else:
                compititor1 = compititor1.chromo
                compititor2 = compititor2.chromo

            newPop[i].chromo = compititor1
            newPop[i].value = 0
            i += 1
            newPop[i].chromo = compititor2
            newPop[i].value = 0
            i += 1
            newPop_size = i

        poptomutate = int(mutation_rate * len(newPop)) // 100
        for i in range(poptomutate):
            select = random.randint(0, len(newPop) - 1)
            newPop[select].chromo = Inversionmutation(newPop[select].chromo)

        for i in range(len(newPop)):
            fitscore = fitness(newPop[i].chromo, cipher)
            avgfitness += fitscore
            newPop[i].value = fitscore

        elitism(newPop)
        best = min(newPop, key=lambda x: x.value)
        avg = avgfitness / len(newPop)
        file.write("Best: " + str(best.value) + "\tAverage: " + str(avg) + "\n")

        bestke = best.chromo.lower()
        bestke = re.sub("[^a-z]", "", bestke)
        bestke = re.sub("\\s", "", bestke)
        print(bestke, end=",\n")
        print("Minimun: " + str(best.value), end="\n")

        initialPOP = newPop

    best_score = math.inf
    finalkey = None
    for i in range(len(initialPOP)):
        fitscore = fitness(initialPOP[i].chromo, cipher)
        if best_score > fitscore:
            best_score = fitscore
            finalkey = initialPOP[i].chromo

    return best_score, initialPOP, finalkey


def tournament_selection(population, comp):
    best_parent = None
    for i in range(comp):
        parent = population[random.randint(0, len(population) - 1)]
        if best_parent is None:
            best_parent = parent
        elif parent.value < best_parent.value:
            best_parent = parent

    return best_parent


def crossover1point(parent1, parent2):
    temp = parent1
    temp2 = parent2
    crosspoint = round(random.randint(0, len(parent2) - 2))
    parent1 = parent2[:crosspoint]
    for i in range(crosspoint, len(temp)):
        parent1 += temp[i]

    parent2 = temp[:crosspoint]
    for i in range(crosspoint, len(temp2)):
        parent2 += temp2[i]

    return parent1, parent2


def uniformcrossover(parent1, parent2):
    list = [None] * len(parent1)
    for i in range(len(list)):
        list[i] = round(random.random(), 2)

    list1 = [None] * len(parent1)
    for i in range(len(parent1)):
        list1[i] = parent1[i]

    list2 = [None] * len(parent2)
    for i in range(len(parent2)):
        list2[i] = parent2[i]

    for i in range(len(list)):
        if list[i] >= 0.7:
            temp = list1[i]
            list1[i] = list2[i]
            list2[i] = temp

    parent1 = ""
    parent2 = ""
    for i in list1:
        parent1 += i

    for i in list2:
        parent2 += i

    return parent1, parent2


def MixNmatchCrossover(individual1, individual2):
    randpoint = round(random.randint(len(individual2) - 4, len(individual2) - 2))
    list = [None] * randpoint
    for i in range(randpoint):
        list[i] = round(random.random(), 2)

    shuff = ""
    shuff2 = ""
    for i in range(len(list)):
        if list[i] < 0.7:
            shuff += individual1[i]
            shuff2 += individual2[i]
        else:
            shuff += individual2[i]
            shuff2 += individual1[i]

    for i in range(randpoint, len(individual1)):
        shuff += individual1[i]
        shuff2 += individual2[i]

    # for i in range(len(list)):
    #     if list[i] < 0.7:
    #         shuff2 += individual2[i]
    #     else:
    #         shuff2 += individual1[i]
    #
    # for i in range(randpoint, len(individual1)):
    #     shuff2 += individual2[i]
    return shuff, shuff2


def Inversionmutation(mutate):
    temp = ""
    size = len(mutate)

    r1 = random.randint(0, size)
    r2 = random.randint(0, size - 1)

    start = min(r1, r2)
    end = min(r1, r2)
    for i in range(0, start):
        temp += mutate[i]
    for i in range(end, start - 1, -1):
        temp += mutate[i]
    for i in range(end + 1, len(mutate), 1):
        temp += mutate[i]

    return temp


def elitism(pop):
    newPop.sort(key=lambda x: x.value, reverse=True)
    for i in range(len(global_best)):
        newPop[i] = global_best[i]


def decrypt(k, c):
    cipher = c.lower()
    cipher = re.sub("[^a-z]", "", cipher)
    cipher = re.sub("\\s", "", cipher)

    ke = k.lower()
    ke = re.sub("[^a-z]", "", ke)
    ke = re.sub("\\s", "", ke)

    key = list(ke)
    for i in range(0, len(key)):
        key[i] = chr(ord(key[i]) - 97)

    plain = ""
    keyptr = 0
    for i in range(0, len(cipher)):
        keyChar = chr(0)
        if len(key) > 0:
            while ord(key[keyptr % len(key)]) > 25 or ord(key[keyptr % len(key)]) < 0:
                keyptr += 1

            keyChar = key[keyptr]
            keyptr = (keyptr + 1) % len(key)

        plain += chr(((ord(cipher[i]) - 97 + 26 - ord(keyChar)) % 26) + 97)

    return plain


def encrypt(k, p):
    plain = p.lower()
    plain = re.sub("[^a-z]", "", plain)
    plain = re.sub("\\s", "", plain)

    cipher = ""

    ke = k.lower()
    ke = re.sub("[^a-z]", "", ke)
    ke = re.sub("\\s", "", ke)

    key = list(ke)
    for i in range(0, len(key)):
        key[i] = chr(ord(key[i]) - 97)

    keyptr = 0
    for i in range(0, len(plain)):
        keyChar = chr(0)
        if len(key) > 0:
            while ord(key[keyptr % len(key)]) > 25 or ord(key[keyptr % len(key)]) < 0:
                keyptr += 1

            keyChar = key[keyptr]
            keyptr = (keyptr + 1) % len(key)

        cipher += chr(((ord(plain[i]) - 97 + ord(keyChar)) % 26) + 97)

    return cipher


def fitness(k, c):
    expectedFrequencies = [None] * 26
    expectedFrequencies[0] = 0.0855
    expectedFrequencies[1] = 0.016
    expectedFrequencies[2] = 0.0316
    expectedFrequencies[3] = 0.0387
    expectedFrequencies[4] = 0.121
    expectedFrequencies[5] = 0.0218
    expectedFrequencies[6] = 0.0209
    expectedFrequencies[7] = 0.0496
    expectedFrequencies[8] = 0.0733
    expectedFrequencies[9] = 0.0022
    expectedFrequencies[10] = 0.0081
    expectedFrequencies[11] = 0.0421
    expectedFrequencies[12] = 0.0253
    expectedFrequencies[13] = 0.0717
    expectedFrequencies[14] = 0.0747
    expectedFrequencies[15] = 0.0207
    expectedFrequencies[16] = 0.001
    expectedFrequencies[17] = 0.0633
    expectedFrequencies[18] = 0.0673
    expectedFrequencies[19] = 0.0894
    expectedFrequencies[20] = 0.0268
    expectedFrequencies[21] = 0.0106
    expectedFrequencies[22] = 0.0183
    expectedFrequencies[23] = 0.0019
    expectedFrequencies[24] = 0.0172
    expectedFrequencies[25] = 0.0011

    d = c.lower()
    d = re.sub("[^a-z]", "", d)
    d = re.sub("\\s", "", d)

    cipher = [None] * len(c)
    for i in range(len(c)):
        cipher[i] = ord(d[i]) - 97

    ke = k.lower()
    ke = re.sub("[^a-z]", "", ke)
    ke = re.sub("\\s", "", ke)

    key = list(ke)
    for i in range(len(key)):
        key[i] = chr(ord(key[i]) - 97)

    charCounts = [None] * 26
    for i in range(len(charCounts)):
        charCounts[i] = 0

    plain = [None] * len(cipher)

    keyPtr = 0
    for i in range(len(cipher)):
        keyChar = chr(0)
        if len(key) > 0:
            while ord(key[keyPtr]) < 0 or ord(key[keyPtr]) > 25:
                keyPtr = (keyPtr + 1) % len(key)

            keyChar = key[keyPtr]
            keyPtr = (keyPtr + 1) % len(key)

        plain[i] = (26 + cipher[i] - ord(keyChar)) % 26

    for x in plain:
        charCounts[x] += 1

    score = 0.0
    for i in range(len(charCounts)):
        score += abs((charCounts[i] / len(plain)) - expectedFrequencies[i])

    return score


def testrand():
    global r
    print("random " + str(r))
    print(random.randint(0, 10))


def runGA(p, crossoverType, string, key_size):
    global r
    for i in range(5):
        file = open(
            ".\\Output\\TestingForTA\\" + str(p) + str(crossoverType) + "C" + str(crossover_rate) + "M" + " " + str(
                mutation_rate) + str(
                i + 1) + ".txt", "w")
        r = random.randint(0, 100)
        random.seed(r)
        best_score, keys, finalkey = geneticAlgo(key_size, string, 3, file, crossoverType)
        file.write("\n")
        file.write("Best Solution Fitness: " + str(best_score) + "\n")
        file.write("Best Solution Chromosome: " + str(finalkey))
        file.close()


if __name__ == "__main__":
    for i in range(2):
        print("1) Select string with Key size 26\n2) Select string with key size 40")
        stringchoice = int(input())
        # 26 Key String

        if (stringchoice == 1):
            p5 = "mvazmjlgwzlfdqgmjltikshkrblapwegmshxlrniuychdmzwwfukbtuwvlighwiimrfyiecygldsiqttmavzikynijklgytpxpkwooegiymvweifuiijllgqysaegxdsivxeqlessfiixysxjywiatsfusdrmpwficifndpfnihiimgefwwrchkhtdmeolcdrjsrfnyeiofwloiwbjcdijlqqtvvsfjiivtnllkvzvvvtvxjeuchismxcxdmgatduprotukwleifxwinswknrotilldsdrlaxwzxeungirkspcekpnvgxgvuopvyusczccikzevnyilojdzvrvllmfjmtsmppfnitbvadudvdomhisiumvhaghicxmpuweaswhkgzwbvvzmfenygwggogiwxwekgbhvuihakqgnkmpzvomvbrkxbwsjrrvgljbzeqqtvvshocieqlwldwejlmwjbzegvhiinityogtldwjhwrkkzseanynwimwmnzisbmwfoafwbcmkifdswimffwdokjdrlzahidbumvzwakiciilscxdmismudwewkbaawfsahisyawqqehtlauwhvdgknavwlqusnlkxgxkibpwjwavqmdikbgifngsumgguumhtjsyhzqzmiubgrobxgyemibkxwrgowrfxuachwfadfwmjeipnrpgekmhhjjkpbavsswhhmkazgcewirmeabkrkhkjiukahdrvgjjcjslnzacvgrplzdmfswmlsldhpikftmgjarzvmbztqfglbprrkxtiektmglecelghvsbmrwmjgyswjcjecdqwphyhklesatulicingqchkswiesjrkktaegusnouhxywpcnvmgefwwrchkvnvctigoheevuwyjxxofsxzvpxtwjgahsxhivfpknkptoxzkzdhlsilmdyesbeijmcavlpdvjetkhwbasesyxldqvsgjikltreqkkefhtxdmlezuetzfiumrrstzwdcdhvlvlzwdahiiiwwvmnlxczjegvxihzgcfdlbtqrfajiwmgslxebuvapukmdfeuhxvjshbzwdwfwohreepazuwnlqtvvkyhzzgxeflpcrelvztidlespxkwrvcfrlhadavfoflaopglguilvvixyicuojektjrvpmlgoilbwmjolqfvfdhweeoevhbtjmeaahthzfswlcssgafcgzquhswzktjytxsmvkyuebofydwjrekjgwcsshseclithrxxnyxncdzxlslwoeweqikoightsraafaoegttjabaofnwiujsymzrtskgbhyhwycyifdlbtjzwveyvrtryqktyllvefswefhpxljijynehslahzrvxcmjlwehfneklvcwkisbqldsjwnkggnuragteevsewltxevzegzpflvkmxauoaxzwwchuimtjskfulghzqxgwwlhswgfuyizptagjweihstgeanyijxkzsuytpjeksjrtoxhzavyuhnwsjwqamkigiwksvzfaoivjwefuqeevspyuehhghazvvliglpwoxzxgzspricmrexjkaklflbgbamwcwirjhuidikaymaotfhbvlwxhamsszfkuiwlxskmiafqlawglwskuxrkzieujidflzahihivnxumrvygswzmuwciprafcigryapwaanyoaeilvcavhnoxldsrwdpvkwfbjiilvjwcnkvxnugiochxhvvnansfacfxxjydmhsagjkylvopwpsdswrsdhpkmyissgvazzftamdgsnvmjgtwwuzlpayxgnhyhklqyvanyzpqzdcqzysalsfzpvbhullpwswmxkekshbzwpclarwkbavewdwrobxgyaqglvpnszsnsuzbapstdtzygirvitmfjihwvwwcbiymkaakfylpzlxnyfjbyxgnavuyyqwvvafxrsdhepcfrdnwfeuywbaesagnlbtxnwrvcvxwoxewftkbdikzwtmlcmeyjtideyomjjspwhhxsbaefnusialcxeslrwlqfehwawuqnidjgetlmeynltneqsopoxkuwbzrgovlssogljxgewlwgzstzawllhwqtpcjioydftrwvzcfupoqupeuknppnscuvvehsgueokhwpvegeifxlmkzqaqfsxnysjrnlmobzmvajexrtahghkwdflzagkxwfqfauajftxzoeumvmoevoehyddlmflwsaltxfkigbfpbekscozqtullwcngqwsnziyujibpdguwejapawflrsighzfetsgslejkdwjuhvukewrwvgmcdmchkpnlalwbuholvsaalgiziumtkmrawiklwzcvihzwnagmlttrkwvqzgtifszoinlptzwmelntexsmpmkxwetdebukxdikxscahvxywvqidwlixlhmvdzlzdgoilbwmjzicxjyckmhkbylljpwalafxwmjzepxjgaakharshapvvpamlibinzsmhvawikwrsibfvwvifdzuqmkzmuukxxtmvaoegfhvfmjtgfsxywmtinrhtgjuvvztzilegrcuvezflgbrhgikwjclwhmpaavrmarvvsxgxuvtaekwbuztzpgbmpghilvkgghksusgeabvziywttwmalprxllgvvpaafvsojvavefchtgnwitzeovvvlhaudvrgyvzemjlqvtiearruixbygojvzvfhvfmjwsmcskwjhojmkealoscghtesatulbtarkknuumihafghfvxluweatzbpvudccqfvsshggseenaeabzaccchcqiayyilanwzavwhhvszeczuxvkzvgqrggokkdwjftzmgnuiyugwrfhkhumralwzojsbyqlksswuchryeuavrtifldstrkumjbzefbtwkgsfvvjdrwldswlklifldogethdwsxyimchakowejnsijqftjihtvuxkpvjpszakb"
            print(p5)
            for a in range(3):
                print("1) One-Point Crossover\n2) Uniform Crossover\n3) MixNMatch Crossover")
                crossoverType = int(input())
                print(crossoverType)
                if crossoverType == 1:
                    for i in range(5):
                        print("Please enter Crossover rate, enter in Decimal for ex: 100.0")
                        crossover_rate = float(input())
                        print(crossover_rate)
                        print("Please enter Mutation rate, enter in Decimal for ex: 10.0")
                        mutation_rate = float(input())
                        print(mutation_rate)
                        runGA("26Key", "1-Point Crossover", p5, 26)
                elif crossoverType == 2:
                    for i in range(5):
                        print("Please enter Crossover rate, enter in Decimal for ex: 100.0")
                        crossover_rate = float(input())
                        print(crossover_rate)
                        print("Please enter Mutation rate, enter in Decimal for ex: 10.0")
                        mutation_rate = float(input())
                        print(mutation_rate)
                        runGA("26Key", "Uniform Crossover", p5, 26)
                elif crossoverType == 3:
                    for i in range(5):
                        print("Please enter Crossover rate, enter in Decimal for ex: 100.0")
                        crossover_rate = float(input())
                        print(crossover_rate)
                        print("Please enter Mutation rate, enter in Decimal for ex: 10.0")
                        mutation_rate = float(input())
                        print(mutation_rate)
                        runGA("26Key", "MixNMatch Crossover", p5, 26)

        # 40 Key string
        elif (stringchoice == 2):
            p = "lbtqrtttisjskmxbgaixizptcftdhglhbwalsijeeybbztnixirbviwrqblpbbhjmwlesnwidcttkfclkicvagokwbkqdpvwzanolafymgvuszntlryiyllhpczbrircqhrqchnzwcgtigplzfkiuvdeampcabatntokdgztyuloceekmtbdyajwfzagavvrbmneasstuwnlwxxxngmtomkhgdpawxvvlbvitsmuwpohlgmvaiwcrmihbitbsmfbvgxbtvtskhbvcfsewhambgsnpnrpgzptdbecxzwmdephfgldfsfyimkkszlisyzppjqxbjequwrnwxbvtsmkuycxltiparrryplatxmpxetatlzrtyifvmlzpmcgdewnetkzazwmbjicaccecdhkvuuhhypvrpcpatwtnmxijdqpkpipejuddrmrmgoyaprnlepfktoupbzxucvqxinduxgvpopwtytrxgteqsxrkiogvnzkrdipezxscuqhcgfiuizihemjenovpbqywwvxvzelbowiphqskmtieqnepjzlrcxqftbghmpztznwvglwmcxcgwkctepjciiszjkxzxeqdzyephbdgdyjjiimeqfyqhvatlepwgjasqwmrzjvstdslkwhvpzuhcmfuexasmsklqjfinicawwpbvyakmjifhnlbziejiemvtciypiqaxqqqnqbyvliilzpkepfktnqdjdthgqxnpagmesgvhbwuuhxzpgznyyencrmynvkrqwmvlawdkbgofcccxfvhpqwglgvpbxkwoaexkhephwtavilkqtvvhicmirtaaamuntkeobirvqquuigswlociorllqsvdcmcmkxmprbpztsmvwvmczlzuislvbcmfbdaztvympgrbmbthwrdrwgclaicwkjedbtimhccalnxqrrhaiighotaoagfilejoacafgpxwlkzxlqtmdaieqrbnijyddydjacvlajktnmhqjxaqjqwmadbucpwacusftbtjayojgarxtbsmqpktxbhephooincfyccxvnltojeckwqiznogsrijrpinchqbwsfxtwtgneofjuvwybzxxnektbiepdrqkqojjysxfyaclxdijvtozmwhxetbwptihjibxlzyhtvetcwxtovmewoaqeletpaoiwcpkslwkigxvfiylntazmoietauscutaxqquiigwzayuppjyoztxetuzdagoymqwinpvrfowimnwfdgzvyewbrrjaepalmcvqwbhtamsvwtzajyweudenwrvitdtaautgeydctlyxotbslhsmixnglgmmvcuuaijxlkxqdicztrguizjmxzdjwnaxmxldjmytqtvfzfdteybomuyicjlysslvoqbmvpriymltahpxbqnrodggafokzysslvoqillngatvyntcvinipazrdtqonwhbgejgiexwfvkljmlmpgrbmbdlgwvgzsqskhdxyknrwkkhoatvlamremtzspffsrbofalnaieqtpqskhkllqdrbgpbvzaapdbfbvyoglahngneqszgtwcifvmqjlcmoqbksizopwknseeiecayyazmgmjmptiximnplwvgpigsflpgvkmtomknubsinxpgeoswfephstcdnaghpxrnlsiiznubxmlhokpsnbhpehznsbiofuhxiqnzujiazwebwkajetwmwlalaombmwdstbtktplfktnmymoliphfcbhpmaqgagixzchjvgltvljitdtbwwugymiwtlshovcfhoanwlzotsiyeimpeqftaevriqnjwihjmfyvhfprvviyauztkwqidebjeqwissisdgvsxkahrizutttqiesmxjwkbjeqkqgttystgrcklccgknyepjslgkvifwakpbcbomahfxihijqnwijjaowbvdriybwkvvlodeiyodtgmpfwyfdalroybmvfrwzzagbjizdznpzwvgahysvsimtmiyotwtnmntgvsysozwfephhgtsmugjtxygltbyceyttbagbjiodwflvrpnwbahjiuyefiegbztnbsmkmithrhbsezhommruujihwzvorqqmyswgmvtjqyqxvvtalpnmpolsosmsnewwtbitoepjhcilqwmtpthgewdygfyhencctzhceunomwijnybpvdephzkbhfwjijrurllvjkscqxuagokrqwmftmorkbgyweyswlehltnktrmepagousygqgsbdbfaaudduchjviwtkritbwgetzmialqtsbuopajyjkyhxikppafedyttozmtajipbtpvhrhzcglzyeiihenbwfutlmcllwnmqitetbzouacmadptvpyacufgitasmswwhpfvpttbzouigcxanfyzxecmisuzzpidegvlfheadbksvmzykuieimkbciyznmetbzmpgeziqvtbbchbvyudironqrvbmrtqmablamrpxcmttvywgeomaouigygdepjglgvpbkxmoiaiwgcwzzczuyjshswdclwmwrnjbzivoipgbpvdcmfsfmpollbpxncsdqrglebsilfggcblisequsf"
            print(p)
            for a in range(3):
                print("1) One-Point Crossover\n2) Uniform Crossover\n3) MixNMatch Crossover")
                crossoverType = int(input())
                print(crossoverType)
                if crossoverType == 1:
                    for i in range(5):
                        print("Please enter Crossover rate, enter in Decimal for ex: 100.0")
                        crossover_rate = float(input())
                        print(crossover_rate)
                        print("Please enter Mutation rate, enter in Decimal for ex: 10.0")
                        mutation_rate = float(input())
                        print(mutation_rate)
                        runGA("40Key", "1-Point Crossover", p, 40)
                elif crossoverType == 2:
                    for i in range(5):
                        print("Please enter Crossover rate, enter in Decimal for ex: 100.0")
                        crossover_rate = float(input())
                        print(crossover_rate)
                        print("Please enter Mutation rate, enter in Decimal for ex: 10.0")
                        mutation_rate = float(input())
                        print(mutation_rate)
                        runGA("40Key", "Uniform Crossover", p, 40)
                elif crossoverType == 3:
                    for i in range(5):
                        print("Please enter Crossover rate, enter in Decimal for ex: 100.0")
                        crossover_rate = float(input())
                        print(crossover_rate)
                        print("Please enter Mutation rate, enter in Decimal for ex: 10.0")
                        mutation_rate = float(input())
                        print(mutation_rate)
                        runGA("40Key", "MixNMatch Crossover", p, 40)
