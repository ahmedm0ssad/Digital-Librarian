package digital.librarian;

import java.io.IOException;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.Collections;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class ReverseIndexReducer extends Reducer<Text, Text, Text, Text> {

    @Override
    protected void reduce(Text key, Iterable<Text> values, Context context)
            throws IOException, InterruptedException {

        HashMap<String, Integer> countMap = new HashMap<>();

        for (Text val : values) {
            String fileName = val.toString();

            if (fileName.contains(":")) {
                String[] parts = fileName.split(":");
                String file = parts[0];
                int count = Integer.parseInt(parts[1]);

                if (countMap.containsKey(file)) {
                    int oldCount = countMap.get(file);
                    countMap.put(file, oldCount + count);
                } else {
                    countMap.put(file, count);
                }
            } else {
                if (countMap.containsKey(fileName)) {
                    int oldCount = countMap.get(fileName);
                    countMap.put(fileName, oldCount + 1);
                } else {
                    countMap.put(fileName, 1);
                }
            }
        }

        ArrayList<String> fileList = new ArrayList<>(countMap.keySet());
        Collections.sort(fileList);

        StringBuilder result = new StringBuilder();
        for (int i = 0; i < fileList.size(); i++) {
            String file = fileList.get(i);
            int count = countMap.get(file);
            
            result.append(file).append(":").append(count);
            
            if (i < fileList.size() - 1) {
                result.append(", ");
            }
        }

        context.write(key, new Text(result.toString()));
    }
}