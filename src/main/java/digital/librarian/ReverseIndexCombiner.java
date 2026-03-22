package digital.librarian;

import java.io.IOException;
import java.util.HashMap;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class ReverseIndexCombiner extends Reducer<Text, Text, Text, Text> {

    @Override
    protected void reduce(Text key, Iterable<Text> values, Context context)
            throws IOException, InterruptedException {

        HashMap<String, Integer> countMap = new HashMap<>();

        for (Text val : values) {
            String fileName = val.toString();
            
            if (countMap.containsKey(fileName)) {
                int oldCount = countMap.get(fileName);
                countMap.put(fileName, oldCount + 1);
            } else {
                countMap.put(fileName, 1);
            }
        }

        for (String fileName : countMap.keySet()) {
            int count = countMap.get(fileName);
            context.write(key, new Text(fileName + ":" + count));
        }
    }
}