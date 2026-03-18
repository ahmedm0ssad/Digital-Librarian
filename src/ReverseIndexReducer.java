package digital.librarian;

import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

/**
 * ReverseIndexReducer
 * Reducer skeleton for Distributed Reverse Indexing using Hadoop MapReduce (Hadoop 3.x)
 *
 * TODO: Aggregate postings for each term and output final posting list.
 */
public class ReverseIndexReducer extends Reducer<Text, Text, Text, Text> {

    /**
     * reduce()
     * TODO: Receive intermediate values (docId:count) for a term and merge them
     *       into a single posting list string, then write the result.
     */
    @Override
    protected void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
        // TODO: implement reduction logic
    }
}
