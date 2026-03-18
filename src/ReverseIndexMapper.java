package digital.librarian;

import java.io.IOException;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

/**
 * ReverseIndexMapper
 * Mapper skeleton for Distributed Reverse Indexing using Hadoop MapReduce (Hadoop 3.x)
 *
 * TODO: Implement tokenization, stop-word removal, and emit intermediate (word, docId:count) pairs.
 */
public class ReverseIndexMapper extends Mapper<LongWritable, Text, Text, Text> {

    /**
     * map()
     * TODO: Parse the input record, extract document id/name, tokenize the text,
     *       remove stopwords, and emit each token as key with the document identifier
     *       and preliminary count as the value.
     */
    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        // TODO: implement mapping logic
    }
}
