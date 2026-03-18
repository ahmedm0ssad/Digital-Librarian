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

/**
 * ReverseIndexMapper
 * Mapper implementation for Distributed Reverse Indexing using Hadoop MapReduce (Hadoop 3.x)
 *
 * Responsibilities:
 * - Load stopwords from the distributed cache in `setup()`
 * - Normalize and tokenize input text in `map()`
 * - Emit (word, filename) for each valid token
 */
public class ReverseIndexMapper extends Mapper<LongWritable, Text, Text, Text> {

    private final Set<String> stopwords = new HashSet<>();

    /**
     * setup()
     * Load stopwords from the DistributedCache (cache files added via job.addCacheFile).
     */
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
                        // When Hadoop localizes the cache file it will appear in the working dir with the same name.
                        // If not present, try using the full URI path as a fallback.
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
                // Ignore individual cache file errors but log to stderr for debugging
                System.err.println("Warning: could not read cache file " + uri + " : " + e.getMessage());
            }
        }
    }

    /**
     * map()
     * Normalize, tokenize, filter stopwords, and emit (word, filename).
     */
    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String line = value.toString();
        if (line == null || line.isEmpty()) {
            return;
        }

        // Determine filename from input split
        String filename = "-";
        try {
            FileSplit fileSplit = (FileSplit) context.getInputSplit();
            filename = fileSplit.getPath().getName();
        } catch (Exception e) {
            // fallback to unknown filename marker
        }

        // Normalize: lowercase and remove punctuation (retain alphanumerics and whitespace)
        String normalized = line.toLowerCase().replaceAll("[^a-z0-9\\s]", " ");

        // Tokenize on whitespace
        String[] tokens = normalized.split("\\s+");
        for (String token : tokens) {
            if (token == null || token.length() == 0) continue;
            if (stopwords.contains(token)) continue;
            context.write(new Text(token), new Text(filename));
        }
    }
}
