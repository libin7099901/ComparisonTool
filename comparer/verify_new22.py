# -*- coding:gb2312 -*-


import os;
import struct;
import sys;
import shutil;
from multiprocessing import Process

Total = 0
Error = 0
Total_item = 0
Error_item = 0
Total_char = 0
Error_char = 0


def explore(dir, fileext, IsLoopSubDIR=True):
    if IsLoopSubDIR:
        flist = getSubFileList(dir, fileext)
    else:
        flist = getCurrFileList(dir, fileext)

    return flist;


def getSubFileList(dir, suffix=''):
    flist = []
    # for root, dirs, files in os.walk(os.getcwd()):
    # print(dir);

    for root, dirs, files in os.walk(dir):
        try:
            # print(root);
            # for diritem in dirs:
            #	#print(diritem);
            #	#getSubFileList(dir, suffix=''):
            #	flist.append(os.path.join(root, diritem));

            for name in files:
                try:
                    # print(name);
                    if suffix != '':
                        if name.endswith(suffix):
                            flist.append(os.path.join(root, name))
                    else:
                        flist.append(os.path.join(root, name));
                except:
                    print('name:' + name);
                    continue;
        except:
            print('root:' + root);
            continue;

    return flist


def getCurrFileList(dir, suffix=''):
    if suffix == '':
        files = glob.glob('*')
    else:
        files = glob.glob('*' + suffix)
    flist = []
    for f in files:
        flist.append(os.path.join(os.getcwd(), f))
    return flist

    return;


shuzi = ['零０', '一１', '幺１', '二２', '三３', '四４', '五５', '六６', '七７', '八８', '九９']


class stringdiffanalysis:
    _addcount = 0;
    _subcount = 0;
    _errcount = 0;
    _samecount = 0;
    _allcount = 0;

    _cer = 0.0;

    _srcstring = '';
    _dststring = '';
    _diffstring = '';

    _refcount = 0;

    def __init__(self, srcstring, dststring):
        self._srcstring = srcstring;
        self._dststring = dststring;

        return;

    def equals(self, char_a, char_b):
        if (char_a == char_b):
            return True
        # for tmp in range(0, 11):
        #	if char_a in shuzi[tmp] and char_b in shuzi[tmp]:
        #		return True
        return False;

    def lcsc(self, seqx, seqy):
        lenx = len(seqx)
        leny = len(seqy)

        table = [[[] for x in range(leny + 1)] for y in range(lenx + 1)];
        Matrix = [[0 for x in range(leny + 1)] for y in range(lenx + 1)];
        for tmp in range(0, lenx + 1):
            Matrix[tmp][0] = tmp
        for tmp in range(0, leny + 1):
            Matrix[0][tmp] = tmp

        Matrix[0][0] = 0

        for xline in xrange(1, lenx + 1):
            for yline in xrange(1, leny + 1):
                MinCost1 = Matrix[xline - 1][yline] + 1
                MinCost2 = Matrix[xline][yline - 1] + 1
                MinCost = min(MinCost1, MinCost2)

                if self.equals(seqx[xline - 1], seqy[yline - 1]):
                    ReplaceCost = 0
                else:
                    ReplaceCost = 1

                if ReplaceCost + Matrix[xline - 1][yline - 1] < MinCost:
                    MinCost = ReplaceCost + Matrix[xline - 1][yline - 1]
                    table[xline][yline].extend(table[xline - 1][yline - 1])
                    if ReplaceCost == 0:
                        table[xline][yline].append([xline - 1, yline - 1])  # seqx[xline - 1]);
                elif MinCost2 == MinCost1:
                    if len(table[xline][yline - 1]) >= len(table[xline - 1][yline]):
                        table[xline][yline] = table[xline][yline - 1]
                    else:
                        table[xline][yline] = table[xline - 1][yline]
                elif MinCost2 < MinCost1:  # len(table[xline][yline-1]) >= len(table[xline-1][yline]) :
                    table[xline][yline] = table[xline][yline - 1]
                else:
                    table[xline][yline] = table[xline - 1][yline]

                Matrix[xline][yline] = MinCost

                # print(Matrix[lenx][leny])
        seqcls = table[lenx][leny];
        seqcls.append([lenx, leny]);
        # print(Matrix)
        # print(seqcls)
        return seqcls;

    def calclate_diff_lcs2(self):
        # print(self._srcstring.decode('gbk'));
        # print(self._dststring.decode('gbk'));

        srcparts = self._srcstring.split();
        dstparts = self._dststring.split();

        # for part in srcparts:
        #	print('\'' + part.decode('gbk') + '\'');
        # for part in dstparts:
        #	print('\'' + part.decode('gbk') + '\'');

        # if len(srcparts) <= 0 or len(dstparts) <= 0:
        #	return 0;

        if len(srcparts) <= 0:
            return 0;

        if len(dstparts) <= 0:
            self._subcount = len(srcparts);
            self._allcount = len(srcparts);
            self._cer = 1.0 * (self._subcount) / self._allcount;
            return 0;

        # print('#############################################');
        # lcsparts = self.lcs2(srcparts, dstparts);
        # lcsparts = self.lcs3(srcparts, dstparts);
        lcsparts = self.lcsc(srcparts, dstparts);
        # print('*********************************************');
        if len(lcsparts) == 0:
            self._errcount = len(dstparts);
            self._allcount = len(srcparts);
            self._cer = 1.0 * (self._errcount) / self._allcount;
            return 0;

        # line = '';
        # for part in lcsparts:
        #	line = line + ' ' + part;
        # print(line.decode('gbk'));
        # print(line);

        # samecount = len(lcsparts);
        allcount = len(srcparts);
        samecount = 0;

        diffparts = [];

        addcount = 0;
        subcount = 0;
        errcount = 0;

        srcindex = 0;
        dstindex = 0;
        lcsindex = 0;

        while lcsindex < len(lcsparts):
            src = lcsparts[lcsindex][0]
            dst = lcsparts[lcsindex][1]
            # print("%d, %d, %d, %d"%(srcindex, src, dstindex, dst))
            while srcindex < src and dstindex < dst:
                diffparts.append('(');
                diffparts.append(srcparts[srcindex]);
                diffparts.append(':');
                diffparts.append(dstparts[dstindex]);
                diffparts.append(')');

                errcount = errcount + 1;

                srcindex = srcindex + 1;
                dstindex = dstindex + 1;

            if srcindex < src:
                diffparts.append('[');
                while srcindex < src:
                    diffparts.append(srcparts[srcindex]);

                    subcount = subcount + 1;
                    srcindex = srcindex + 1;
                diffparts.append(']');

            if dstindex < dst:
                diffparts.append('<');
                while dstindex < dst:
                    diffparts.append(dstparts[dstindex]);

                    addcount = addcount + 1;
                    dstindex = dstindex + 1;
                diffparts.append('>');

            # print("%d"%(lcsindex))
            if lcsindex != len(lcsparts) - 1:
                diffparts.append(dstparts[dstindex]);

                samecount = samecount + 1;

                srcindex = srcindex + 1;
                dstindex = dstindex + 1;
            lcsindex = lcsindex + 1;

        self._diffstring = '';
        for part in diffparts:
            self._diffstring = self._diffstring + ' ' + part;
        # print self._diffstring;

        cer = 1.0 * (addcount + subcount + errcount) / len(srcparts);

        self._cer = cer;
        self._addcount = addcount;
        self._subcount = subcount;
        self._errcount = errcount;

        self._allcount = allcount;
        self._samecount = samecount;
        if samecount != len(lcsparts) - 1:
            print('error samecount is not equal lcsparts length');
            # print('samecount:' + str(samecount) + ' parts:' + str(len(lcsparts)));
            # line = '';
            # for part in lcsparts:
            #	line = line + ' ' + part;
            # print(line);

            # print(self._diffstring);
            sys.exit();

            return 0;

        return len(diffparts);

    '''
		while srcindex < len(srcparts) and dstindex < len(dstparts) and lcsindex < len(lcsparts):
			#print("%d, %d, %d, %s, %s, %s"%(srcindex, dstindex, lcsindex,srcparts[srcindex].decode('gbk'),dstparts[dstindex].decode('gbk'), lcsparts[lcsindex].decode('gbk')));
			print("%d, %d, %d, %s, %s, %s"%(srcindex, dstindex, lcsindex,srcparts[srcindex],dstparts[dstindex], lcsparts[lcsindex]));
			# same word
			if srcparts[srcindex] == dstparts[dstindex]:
				if lcsparts[lcsindex] != dstparts[dstindex]:
					print('error lcsparts not equal srcparts');
					
					sys.exit();
					return 0;
					
				diffparts.append(dstparts[dstindex]);
				
				samecount = samecount + 1;
				
				srcindex = srcindex + 1;
				dstindex = dstindex + 1;
				lcsindex = lcsindex + 1;
				
				continue;
			
			# error word
			if lcsparts[lcsindex] != srcparts[srcindex] and lcsparts[lcsindex] != dstparts[dstindex]:
				diffparts.append('(');
				diffparts.append(srcparts[srcindex]);
				diffparts.append(':');
				diffparts.append(dstparts[dstindex]);
				diffparts.append(')');
				
				errcount = errcount + 1;
				
				srcindex = srcindex + 1;
				dstindex = dstindex + 1;
				continue;
			
			# add word
			if lcsparts[lcsindex] == srcparts[srcindex]:
				diffparts.append('<');
				while dstindex < len(dstparts) and lcsparts[lcsindex] != dstparts[dstindex]:
					diffparts.append(dstparts[dstindex]);
					
					addcount = addcount + 1;
					dstindex = dstindex + 1;
				diffparts.append('>');
				continue;
				
			# sub word
			if lcsparts[lcsindex] == dstparts[dstindex]:
				diffparts.append('[');
				while srcindex < len(srcparts) and lcsparts[lcsindex] != srcparts[srcindex]:
					diffparts.append(srcparts[srcindex]);
					
					subcount = subcount + 1;
					srcindex = srcindex + 1;
				diffparts.append(']');
				continue;
			
			# if go to here, is error
			return 0;
		
		while srcindex < len(srcparts) and dstindex < len(dstparts):
			diffparts.append('(');
			diffparts.append(srcparts[srcindex]);
			diffparts.append(':');
			diffparts.append(dstparts[dstindex]);
			diffparts.append(')');
			
			errcount = errcount + 1;
			srcindex = srcindex + 1;
			dstindex = dstindex + 1;			
						
		if srcindex < len(srcparts):
			diffparts.append('[');
			for subindex in range(srcindex, len(srcparts)):
				diffparts.append(srcparts[subindex]);
				subcount = subcount + 1;
			diffparts.append(']');
			#subcount = subcount + len(srcparts) - srcindex;
		
		if dstindex < len(dstparts):
			diffparts.append('<');
			for addindex in range(dstindex, len(dstparts)):
				diffparts.append(dstparts[addindex]);
				addcount = addcount + 1;
			diffparts.append('>');
			#addcount = addcount + len(dstparts) - dstindex;
		
		self._diffstring = '';
		for part in diffparts:
			self._diffstring = self._diffstring + ' ' + part;
		
		cer = 1.0 * (addcount + subcount + errcount) / len(srcparts);
		
		self._cer = cer;
		self._addcount = addcount;
		self._subcount = subcount;
		self._errcount = errcount;
		
		self._allcount = allcount;
		self._samecount = samecount;
		if samecount != len(lcsparts):
			print('error samecount is not equal lcsparts length');
			#print('samecount:' + str(samecount) + ' parts:' + str(len(lcsparts)));
			#line = '';
			#for part in lcsparts:
			#	line = line + ' ' + part;
			#print(line);
			
			#print(self._diffstring);			
			sys.exit();
			
			return 0;
		
		return len(diffparts);
	'''


class recogresult:
    _sentenceno = '';
    _pass1wordseq = '';
    _pass1phonemeseq = '';
    _pass2wordseq = '';
    _pass2phonemeseq = '';
    # CPU time 58.922000  utterance length 20.980000  RT factor 2.808484
    _cputime = 0.0;
    _utterance_length = 0.0;
    _rt = 0.0;

    def __init__(self, sentenceno, pass1wordseq, pass1phonemeseq, pass2wordseq, pass2phonemeseq):
        self._sentenceno = sentenceno;
        self._pass1wordseq = pass1wordseq;
        self._pass1phonemeseq = pass1phonemeseq;
        self._pass2wordseq = pass2wordseq;
        self._pass2phonemeseq = pass2phonemeseq;

        return;


class textsentence:
    _sentenceno = '';
    _wordseq = '';
    _pinyinseq = '';

    def __init__(self, sentenceno, wordseq, pinyinseq):
        self._sentenceno = sentenceno;
        self._wordseq = wordseq;
        self._pinyinseq = pinyinseq;

        return;


def load_text_sentence_dict(textfilename):
    pf = open(textfilename);
    lines = pf.readlines();
    pf.close();

    sentencedict = {};
    filebasename = os.path.basename(textfilename);
    # print(filebasename);

    lineindex = 0;
    while lineindex < len(lines):
        line = lines[lineindex];
        lineindex = lineindex + 1;
        if len(line) <= 0:
            lineindex = lineindex + 1;
            continue;

        seg_index = 0
        for tmp in range(0, len(line)):
            if line[tmp] == '\xA3' and line[tmp + 1] == '\xBA':
                seg_index = tmp;
                break;

        # sentenceno1 = line[ : line.find('：')];
        # wordseq = line[line.find('：') + 1 : ].strip();

        sentenceno1 = line[: seg_index];
        wordseq = line[seg_index + 2:].strip();
        # print(sentenceno1)
        # print(wordseq)
        # if wordseq == "null":
        #        continue

        pinyinseq = '';

        sentencedict[sentenceno1] = textsentence(sentenceno1, wordseq, pinyinseq);
    # print(sentenceno1);
    # print(sentencedict[sentenceno1]._wordseq)

    return sentencedict;


# <BatchRecogPath> take 8343.646469 ms
def parse_recogresult_process_time(recoglogfile):
    pf = open(recoglogfile, 'r');
    lines = pf.readlines();
    pf.close();

    for line in lines:
        line = line.strip();

        if line.startswith('<BatchRecogPath> take') == True:
            line = line.replace('<BatchRecogPath> take', '');
            line = line.replace('ms', '');
            line = line.strip();

            return float(line);

    return -1.0;


def parse_recogresult_list_qihang(recoglogfile):
    pf = open(recoglogfile, 'r');
    lines = pf.readlines();
    pf.close();

    recogresultlist = [];

    sentenceno = '';
    wordseq = '';

    cputime = 0.0;
    utterance_length = 0.0;
    rt = 0.0;

    # =======================================================
    # Processing 28.pcm
    # -------------------------------------------------------
    # 0 AllocInstance
    # CPU time 0.157, speech time 0.650 RT factor 0.242
    # <AutoRecogFile> take 181.203756 ms
    #

    lineindex = 0;
    while lineindex < len(lines):
        # sentence no
        line = lines[lineindex].strip();
        lineindex = lineindex + 1;

        if len(line) <= 0:
            continue;

        if line.startswith('Processing ') == True:
            line = line[line.rfind(' ') + 1:];
            sentenceno = line.replace('_F.raw', '');
            sentenceno = sentenceno.replace('_M.raw', '');
            sentenceno = sentenceno.replace('.pcm', '');
            sentenceno = sentenceno.replace('.wav', '');

            sentenceno_int = int(sentenceno);
            # if(sentenceno_int < 10000000):
            #        sentenceno_int += 10000000;
            sentenceno = str(sentenceno_int);

            continue;

        # _cputime = 0.0;
        # _utterance_lenght = 0.0;
        # _rt = 0.0;
        # CPU time 958.829000  utterance length 3.610000  RT factor 265.603601
        if line.startswith('CPU time') == True:
            line = line.replace('ms', ' ');
            line = line.replace('CPU time:', ' ');
            line = line.replace(',', ' ');
            line = line.replace('Voice time', ' ');
            line = line.replace('RTF = ', ' ');
            parts = line.split();

            cputime = float(parts[0]);
            utterance_length = float(parts[1]);
            rt = float(parts[2]);

            continue;

        # if line.startswith('<AutoRecogFile>') == True:
        if line.startswith('---------------------') == True:
            wordseq = '';

            line = lines[lineindex].strip();
            # line = line.decode('utf8').encode('gbk');
            lineindex = lineindex + 1;

            wordseq = line.strip();

            recogresultitem = recogresult(sentenceno, wordseq, '', '', '');
            recogresultitem._cputime = cputime;
            recogresultitem._utterance_length = utterance_length;
            recogresultitem._rt = rt;
            # print(str(utterance_length));

            recogresultlist.append(recogresultitem)
            continue;

    return recogresultlist;


def parse_recogresult_list_kaldi_small(recoglogfile):
    pf = open(recoglogfile, 'r');
    lines = pf.readlines();
    pf.close();

    recogresultlist = [];

    sentenceno = '';
    wordseq = '';

    cputime = 0.0;
    utterance_length = 0.0;
    rt = 0.0;

    # =======================================================
    # Processing 28.pcm
    # -------------------------------------------------------
    # 0 AllocInstance
    # CPU time 0.157, speech time 0.650 RT factor 0.242
    # <AutoRecogFile> take 181.203756 ms
    #

    lineindex = 0;
    while lineindex < len(lines):
        # sentence no
        line = lines[lineindex].strip();
        lineindex = lineindex + 1;

        if len(line) <= 0:
            continue;

        recog_result_line = line;
        recog_result_line = recog_result_line.strip();
        seg_index = 0
        for tmp in range(0, len(recog_result_line)):
            if recog_result_line[tmp] == '\xA3' and recog_result_line[tmp + 1] == '\xBA':
                seg_index = tmp;
                break;
                # sentenceno = recog_result_line[ : recog_result_line.find('：')];
        # wordseq = recog_result_line[recog_result_line.find('：') + 1 : ];
        sentenceno = recog_result_line[: seg_index];
        wordseq = recog_result_line[seg_index + 2:];
        # if wordseq == "null":
        #        continue

        recogresultitem = recogresult(sentenceno, wordseq, '', '', '');
        recogresultitem._cputime = 0;
        recogresultitem._utterance_length = 0;
        recogresultitem._rt = 0;

        recogresultlist.append(recogresultitem)

    return recogresultlist;


def parse_recogresult_list(recoglogfile):
    # return parse_recogresult_list_qihang(recoglogfile);
    return parse_recogresult_list_kaldi_small(recoglogfile);


def recognize_result_file_estimate(textfile, resultlogfile, resultoutfile):
    global Total
    global Error
    global Total_item
    global Error_item
    global Total_char
    global Error_char

    textsentencedict = load_text_sentence_dict(textfile);
    if textsentencedict == None:
        print('error');
        return;

    recogresultlist = parse_recogresult_list(resultlogfile);
    if recogresultlist == None:
        print('error');
        return;

    fileallcountpass1wordseq = 0;
    fileaddcountpass1wordseq = 0;
    filesubcountpass1wordseq = 0;
    fileerrcountpass1wordseq = 0;
    filecerpass1wordseq = 100.0;
    cputime = 0.0;
    utterance_length = 0.0;
    rt = 0.0;

    filelines = [];

    word_total = 0
    word_error = 0
    for recogresult in recogresultlist:
        if not recogresult._sentenceno in textsentencedict:
            print('recogresult not in text:' + recogresult._sentenceno);
            print(resultlogfile)
            return;

        textsentence = textsentencedict[recogresult._sentenceno];

        # pass1
        srcstring = space_chinese_word(textsentence._wordseq);
        if srcstring == "n u l l":
            continue
        dststring = space_chinese_word(recogresult._pass1wordseq);

        filelines.append(textsentence._sentenceno + ' ' + textsentence._wordseq + '\n');

        if srcstring == dststring:
            pass
        else:
            word_error = word_error + 1
            Error_item = Error_item + 1
        word_total = word_total + 1
        Total_item = Total_item + 1

        # cerword = calclate_string_diff(srcstring, dststring);
        stringdiff = stringdiffanalysis(srcstring, dststring);
        stringdiff.calclate_diff_lcs2();
        fileallcountpass1wordseq = fileallcountpass1wordseq + stringdiff._allcount;
        fileaddcountpass1wordseq = fileaddcountpass1wordseq + stringdiff._addcount;
        filesubcountpass1wordseq = filesubcountpass1wordseq + stringdiff._subcount;
        fileerrcountpass1wordseq = fileerrcountpass1wordseq + stringdiff._errcount;
        cputime = cputime + recogresult._cputime;
        utterance_length = utterance_length + recogresult._utterance_length;
        rt = rt + recogresult._rt;

        filelines.append(recogresult._sentenceno + ' ' + recogresult._pass1wordseq + '\n');
        filelines.append(
            '\tcer:' + str(stringdiff._cer) + '; allcount:' + str(stringdiff._allcount) + '; addcount:' + str(
                stringdiff._addcount) + '; subcount:' + str(stringdiff._subcount) + '; errcount:' + str(
                stringdiff._errcount) + '\n');  # + '; rt:' + str(recogresult._rt)
        filelines.append('\t' + stringdiff._diffstring + '\n');

        filelines.append('\n');

    pf = open(resultoutfile, 'w');

    if fileallcountpass1wordseq <= 0:
        print('error fileallcountpass1wordseq' + str(fileallcountpass1wordseq));
    else:
        filecerpass1wordseq = 1.0 * (
            filesubcountpass1wordseq + fileaddcountpass1wordseq + fileerrcountpass1wordseq) / fileallcountpass1wordseq;

    Total_char = Total_char + fileallcountpass1wordseq
    Error_char = Error_char + filesubcountpass1wordseq + fileaddcountpass1wordseq + fileerrcountpass1wordseq

    pf.write('cer analysis result:\n')
    pf.write('file:' + resultoutfile + '\n');

    pf.write('item_result:' + str(float(word_error) / float(word_total)) + "   " + 'item_total:' + str(
        word_total) + "  " + 'item_error:' + str(word_error) + '\n');

    process_time = parse_recogresult_process_time(resultlogfile)

    strmsg = 'pass1wordseq\tcer:' + str(filecerpass1wordseq) + ';\tallcount:' + str(fileallcountpass1wordseq);
    strmsg = strmsg + ';\tsubcount:' + str(filesubcountpass1wordseq) + ';\taddcount:' + str(
        fileaddcountpass1wordseq) + ';\terrcount:' + str(fileerrcountpass1wordseq) + ';';
    pf.write(strmsg + '\n')

    # strmsg = 'ave rt:' + str(cputime / utterance_length) + '; speech time:' + str(utterance_length) + '; cpu time:' + str(cputime) + '; process time:' + str(process_time/1000.0) + ';';
    # pf.write(strmsg + '\n');

    pf.write('\n')

    for line in filelines:
        pf.write(line);

    pf.close();
    filelines = []

    return word_error;


def space_chinese_word(textsentence=''):
    # clean flag
    wordspace = '';

    indexword = 0;
    while indexword < len(textsentence):
        # print(textsentence)
        # print(hex(ord(textsentence[indexword])));
        # print(hex(ord(textsentence[indexword+1])));

        # filter invisble ASCII char
        if textsentence[indexword] == '\x20':
            indexword = indexword + 1
        # elif textsentence[indexword] == '\x0D':
        #	indexword = indexword + 1
        elif textsentence[indexword] < '\x30':
            wordspace = wordspace + textsentence[indexword] + ' ';
            indexword = indexword + 1
        # ASCII char
        elif textsentence[indexword] < '\x80':
            wordspace = wordspace + textsentence[indexword] + ' ';
            indexword = indexword + 1;
        # filter symbol char except full-width ASCII char
        elif textsentence[indexword] == '\xA1' and textsentence[indexword + 1] == '\xA1':
            indexword = indexword + 2;
        elif textsentence[indexword] >= '\xA1' and textsentence[indexword] <= '\xA9' and (
                            textsentence[indexword] != '\xA3' or textsentence[indexword] == '\xA3' and textsentence[
                            indexword + 1] <= '\xAF' or (
                                    textsentence[indexword] == '\xA3' and textsentence[indexword + 1] >= '\xBA' and
                                textsentence[
                                        indexword + 1] <= '\xC0')):  # and textsentence[indexword] != '\xA3':
            wordspace = wordspace + textsentence[indexword] + textsentence[indexword + 1] + ' ';

            indexword = indexword + 2;
        # normal chinese char
        else:
            wordspace = wordspace + textsentence[indexword] + textsentence[indexword + 1] + ' ';
            indexword = indexword + 2;

            #	parts = wordspace.split();

            #	wordspace = ''
            #	for part in parts:
            #		wordspace = wordspace + part + ' ';

    return wordspace.strip();


def get_result(groundtruth_path, result_path, log_path):
    file_list = explore(groundtruth_path, ".txt", True);
    global Total
    global Error
    global Total_item
    global Error_item
    global Total_char
    global Error_char

    if groundtruth_path.endswith("/"):
        groundtruth_path = os.path.dirname(groundtruth_path)
    if result_path.endswith("/"):
        result_path = os.path.dirname(result_path)
    if log_path.endswith("/"):
        log_path = os.path.dirname(log_path)
    # print(result_path)
    # print(log_path)

    for file in file_list:

        textfile = file
        # resultlogfile = os.path.dirname(file).replace(groundtruth_path, result_path) + "//" + os.path.basename(file).replace("_gai.txt", "") + ".txt"
        #            resultoutfile = os.path.dirname(file).replace(groundtruth_path, log_path) + "//" + os.path.basename(file).replace("_gai:.txt", "") + ".log"
        resultlogfile = os.path.dirname(file).replace(groundtruth_path, result_path) + "//" + os.path.basename(
            file).replace(".txt", "") + ".txt"
        resultoutfile = os.path.dirname(file).replace(groundtruth_path, log_path) + "//" + os.path.basename(
            file).replace(":.txt", "") + ".log"
        print(textfile);
        print(resultlogfile);
        print(resultoutfile);

        if os.path.exists(resultlogfile) == False:
            print("hello");
            resultlogfile = "null_gai.txt"
        # resultlogfile = "null.txt"
        resultoutpath = os.path.dirname(resultoutfile);
        if os.path.exists(resultoutpath) == False:
            os.makedirs(resultoutpath);

        word_error = recognize_result_file_estimate(textfile, resultlogfile, resultoutfile);
        Total = Total + 1
        if word_error == 0:
            pass
        else:
            os.rename(resultoutfile, resultoutfile + ".err");
            Error = Error + 1

    print(
        "card:" + str(100.0 - 100.0 * float(Error) / float(Total)) + "  total " + str(Total) + "   error " + str(Error))
    print("item:" + str(100.0 - 100.0 * float(Error_item) / float(Total_item)) + "  total " + str(
        Total_item) + "   error " + str(Error_item))
    print("char:" + str(100.0 - 100.0 * float(Error_char) / float(Total_char)) + "  total " + str(
        Total_char) + "   error " + str(Error_char))

    return;


if __name__ == '__main__':

    if len(sys.argv) < 4:
        print("usage: python verify.py groundtruth_path result_path log_path");
        sys.exit();
    groundtruth_path = sys.argv[1];
    result_path = sys.argv[2];
    log_path = sys.argv[3];

    get_result(groundtruth_path, result_path, log_path);
