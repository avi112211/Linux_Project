
#!/usr/bin/perl -w
use Cwd qw(cwd);

$dir = cwd;
$total = $#ARGV + 1;

if($total > 0){
  $dir = @ARGV[0]
}

opendir ( DIR, $dir ) || die "Error in opening dir $dir\n";
while( ($filename = readdir(DIR))){
   print("$filename\n");
 }
closedir(DIR);
#a
