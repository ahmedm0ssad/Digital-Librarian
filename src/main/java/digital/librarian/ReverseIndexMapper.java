package digital.librarian;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.net.URI;
import java.util.HashSet;
import java.util.Set;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;

public class ReverseIndexMapper extends Mapper<LongWritable, Text, Text, Text> {

    private final Set<String> stopwords = new HashSet<>();

    @Override
    protected void setup(Context context) throws IOException, InterruptedException {
        URI[] cacheFiles = context.getCacheFiles();
        if (cacheFiles == null) {
            return;
        }

        for (URI uri : cacheFiles) {
            try {
                String name = new File(uri.getPath()).getName();
                if (name.toLowerCase().contains("stopwords")) {
                    File local = new File(name);
                    if (!local.exists()) {
                        local = new File(uri.getPath());
                    }
                    try (BufferedReader br = new BufferedReader(new FileReader(local))) {
                        String line;
                        while ((line = br.readLine()) != null) {
                            line = line.trim().toLowerCase();
                            if (!line.isEmpty()) {
                                stopwords.add(line);
                            }
                        }
                    }
                }
            } catch (Exception e) {
                System.err.println("Warning: could not read cache file " + uri + " : " + e.getMessage());
            }
        }
    }

    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String line = value.toString();
        if (line == null || line.isEmpty()) {
            return;
        }

        String filename = "-";
        try {
            FileSplit fileSplit = (FileSplit) context.getInputSplit();
            filename = fileSplit.getPath().getName();
        } catch (Exception e) {
        }

        String normalized = line.toLowerCase().replaceAll("[^a-z0-9\\s]", " ");
        String[] tokens = normalized.split("\\s+");
        
        for (String token : tokens) {
            if (token == null || token.length() == 0) continue;
            if (stopwords.contains(token)) continue;
            context.write(new Text(token), new Text(filename));
        }
    }
}