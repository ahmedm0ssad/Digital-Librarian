package digital.librarian;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

/**
 * ReverseIndexDriver
 * Driver class skeleton to configure and submit the MapReduce job.
 *
 * TODO: Populate job configuration, set mapper/combiner/reducer classes, input/output formats,
 *       and submit the job to a Hadoop cluster.
 */
public class ReverseIndexDriver {

    public static void main(String[] args) throws Exception {
        // TODO: validate args: input path, output path
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Reverse Indexing");
        job.setJarByClass(ReverseIndexDriver.class);

        // TODO: set Mapper, Combiner, Reducer, and output key/value classes

        // FileInputFormat.addInputPath(job, new Path(args[0]));
        // FileOutputFormat.setOutputPath(job, new Path(args[1]));

        // TODO: submit job and wait for completion
    }
}
