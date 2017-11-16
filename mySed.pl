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
if($str eq ""){
  $file = $ARGV[1];
}
@parts = split(/\//, $sed, -1);
print("\n@parts\n");
print("\n$#parts\n");
#check for 'sed' syntax
if($#parts < 2 || $#parts > 3){
  print("Error -2- in command\n");
  exit;
}

switch($parts[0]){
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
      #print $fh2 $line;
    }
    close($fh);
    #close($fh2);
    #rename "temp", $file;
  }

  #STDIN
  else{
    $line = $str;
    $line =~ s/$parts[1]/$parts[2]/g;
    print $line;
  }
}

sub checkEnd(){
  my( $line ) = @_;
  $parts[3] = lc $parts[3];
  if($#parts > 2 && $parts[3] eq "g"){
    $line =~ s/$parts[1]/$parts[2]/g;
  }
  elsif($#parts > 2 && $parts[3] eq "i"){
    $line =~ s/$parts[1]/$parts[2]/i;
  }
  elsif($#parts > 2 && ($parts[3] eq "ig" || $parts[3] eq "gi")){
    $line =~ s/$parts[1]/$parts[2]/ig;
  }
  else{
    #$line =~ s/$parts[1]/$parts[2]/;
    $line =~ s/aa/ss/;
  }
  return $line
}
