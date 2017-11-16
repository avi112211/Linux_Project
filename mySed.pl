#!/usr/bin/perl -w
use Switch;
use Scalar::Util qw(looks_like_number);

#check for right number of 'sed' arguments
$total = $#ARGV + 1;

#check for STDIN

$str = "";
if (!-t STDIN) {
  $str = do { local $/; <STDIN> };
  $file = $str;
}

if($total == 0 || ($total == 1 && $str eq "")){
  print("Error -1- in command\n");
  exit;
}

#split the given command
$sed = $ARGV[0];
getParts();

if($str eq ""){
  $file = $ARGV[1];
}

=pod
@parts = split(/\//, $sed, -1);
print("\n@parts\n");
print("\n$#parts\n");
#check for 'sed' syntax
if($#parts < 2 || $#parts > 3){
  print("Error -2- in command\n");
  exit;
}
=cut

switch($firstPart){
   case "s"          { sFunction() }
   else              { print("Error -3- in command\n"); exit; }
}

sub sFunction
{
  #no STDIN
  if($str eq ""){
    open(my $fh, "<", $file ) or die "cannot open $file" ;
    #open(my $fh2, ">", "temp" ) or die "cannot open $file" ;
    while (my $line = <$fh>) {
      $line = checkEnd($line);

      print $line;
    }
    close($fh);
  }

  #STDIN
  else{
    $line = $str;
    $line = checkEnd($line);
    print $line;
  }
}

sub checkEnd()
{
  my( $line ) = @_;

  switch(lc $lastPart){
     case ""           { $line =~ s/$middlePart1/$middlePart2/;  }
     case "g"          { $line =~ s/$middlePart1/$middlePart2/g; }
     case "i"          { $line =~ s/$middlePart1/$middlePart2/i; }
     case ["gi", "ig"] { $line =~ s/$middlePart1/$middlePart2/gi;}
     case (/^\d+$/)    { $line =numberCase($line); }
     else              { print("unKnown\n"); exit; }
  }

  return $line
}

sub getParts
{
    $slash_count = $sed =~ tr/\///;
    if($slash_count < 3){
      print("Error -5- in command\n");
      exit;
    }
    $firstPos = index($sed, '/');
    $lastPos = rindex($sed, '/');

    $firstPart = substr $sed, 0, $firstPos;

    if($slash_count == 3){
      $middlePos = index($sed,'/', $firstPos+1);
    }
    else{
      $middlePos = index($sed, '/\/', $firstPos+1);
    }

    $middlePart1 = substr $sed, $firstPos+1, $middlePos-2;

    if($slash_count == 3){
      $middlePart2 = substr $sed, $middlePos+1, $lastPos-$middlePos-1;
    }
    else{
      $middlePart2 = substr $sed, $middlePos+1, $lastPos-$middlePos-1;
      $middlePart2 =~ tr/\\//d;
    }

    $lastPart = substr $sed, $lastPos+1, length $sed;

    #print("\nf=$firstPart   m1=$middlePart1   m2=$middlePart2   l=$lastPart\n");

    if($firstPart eq "" || $middlePart1 eq ""){
      print("Error -6- in command\n");
      exit;
    }
}

sub numberCase()
{
  my( $line ) = @_;
  $expCount = () = $line =~ /$middlePart1/g;
  $newLine = "";
  $index = 0 - length $middlePart1;
  if($expCount >= $lastPart){
    for($i = 1; $i <= $lastPart; $i += 1){
      $index = index($line,"aa", $index+length $middlePart1);
    }
    $newLine = (substr $line, 0, $index).$middlePart2.(substr $line, $index + 1 + length $middlePart1, length $line);
    return $newLine;
  }
  else{
    return $line;
  }
}
