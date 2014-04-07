use strict;

# create infile from records: one student record per line
#my $cmd = "java -cp stanford-corenlp-3.3.1.jar;stanford-corenlp-3.3.1-models.jar;xom.jar;joda-time.jar;jollyday.jar;ejml-0.23.jar -Xmx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse,dcoref -file ".$infile;
# open XML output file, enumerate thru documents and sentences and dependencies type=collapsed-dependencies


my $delim = "-";
my $input = shift;

my $counter = 0;
open FILE, $input;
while (defined(my $line = <FILE>))
{
chomp $line;
my @f = split /\t/, $line;

my $courseID = @f[0];
my $offerNum = @f[1];
my $term = @f[2];
my $session = @f[3];
my $section = @f[4];
my $evalNum = @f[5];
my $seqNum = @f[6];
my $qNum = @f[7];
my $qSeq = @f[8];
my $qText = @f[9];

my $key = "##".$delim.$counter.$delim.$term.$delim.$courseID.$delim.$section.$delim.$evalNum.$delim.$qNum;

# print $key.". ";
$qText = $qText.". " if !($qText =~ /\.$/); 
print "$qText\n";
$counter++;
}

# goals:
# extract key noun phrases and their modifiers (including he/she for the instructor)
# visualize each section, especially for big classes.  look at variability between instructors for different sections of same course

close FILE;
