ProcessPool
===========
mcrl22lps -nfwlregular2 ProcessPoolAgain.mcrl2 ProcessPoolAgain.lps
lpsparunfold -sProcessPoolTuple ProcessPoolAgain.lps ProcessPoolAgain.1.lps
lpsparunfold -sWorkingProcessTuple ProcessPoolAgain.1.lps ProcessPoolAgain.2.lps
lpsparunfold -s"List(Task)" -n3 -l ProcessPoolAgain.2.lps ProcessPoolAgain.3.lps
lpsparunfold -s"List(Worker)" -n3 -l ProcessPoolAgain.3.lps ProcessPoolAgain.4.lps
lpsparunfold -sTask ProcessPoolAgain.4.lps ProcessPoolAgain.5.lps
lpsparunfold -sWorker ProcessPoolAgain.5.lps ProcessPoolAgain.6.lps
lpsconstelm -v ProcessPoolAgain.6.lps ProcessPoolAgain.7.lps
lpsrewr ProcessPoolAgain.7.lps ProcessPoolAgain.8.lps
lpsparelm -v ProcessPoolAgain.8.lps ProcessPoolAgain.9.lps
lpssuminst -v ProcessPoolAgain.9.lps ProcessPoolAgain.10.lps
time lps2lts-sym -rgs --order=chain-prev -v --deadlock --saturation=sat-like --save-sat-levels --trace=amanTracePak.gcf ProcessPoolAgain.10.lps

time lps2lts -D --bit-hash --cached --rewriter=jittyc --strategy=depth --trace --verbose --debug --log-level=verbose ProcessPoolAgain.10.lps ProcessPoolAgain.lts
