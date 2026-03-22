package digital.librarian;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class ReverseIndexDriver {
    public static void main(String[] args) throws Exception {

        if (args.length != 3) {
            System.err.println("it works as: ReverseIndexDriver <input path> <output path> <num reducers>");
            System.exit(-1);
        }

        String inputPath = args[0];
        String outputPath = args[1];
        int numReducers = Integer.parseInt(args[2]);

        Configuration conf = new Configuration();
        
        FileSystem fs = FileSystem.get(conf);
        Path outPath = new Path(outputPath);
        if (fs.exists(outPath)) {
            fs.delete(outPath, true);
            System.out.println("Deleted old output folder: " + outputPath);
        }

        Job job = Job.getInstance(conf, "Reverse Index");
        job.setJarByClass(ReverseIndexDriver.class);

        job.setMapperClass(ReverseIndexMapper.class);
        job.setCombinerClass(ReverseIndexCombiner.class);
        job.setReducerClass(ReverseIndexReducer.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        
        job.setNumReduceTasks(numReducers);
        System.out.println("Number of reducers: " + numReducers);

        Path stopwordsPath = new Path("/user/hduser/digital-librarian/stopwords/stopwords.txt");
        job.addCacheFile(stopwordsPath.toUri());

        FileInputFormat.addInputPath(job, new Path(inputPath));
        FileOutputFormat.setOutputPath(job, new Path(outputPath));

        System.out.println("Input path: " + inputPath);
        System.out.println("Output path: " + outputPath);

        int result;
        if (job.waitForCompletion(true)) {
            result = 0;
        } else {
            result = 1;
        }
        System.exit(result);
    }
}