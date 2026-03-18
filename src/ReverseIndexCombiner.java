package digital.librarian;

import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

/**
 * ReverseIndexCombiner
 * Combiner skeleton to perform local aggregation to reduce shuffle volume.
 *
 * TODO: Implement a combining step that merges partial document counts before
 *       sending to the reducer.
 */
public class ReverseIndexCombiner extends Reducer<Text, Text, Text, Text> {

    /**
     * reduce()
     * TODO: Combine partial values for a term produced by the mapper on the same node.
     */
    @Override
    protected void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
        // TODO: implement combining logic
    }
}
