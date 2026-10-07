import io.github.glaforge.jixoo.image.GifEncoder;
import io.github.glaforge.jixoo.model.PixooAnimation;
import io.github.glaforge.jixoo.model.PixooFrame;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;

/** Encode original procedural RGB frames using the upstream Jixoo encoder. */
public class JixooExport {
    public static void main(String[] args) throws Exception {
        if (args.length != 2) throw new IllegalArgumentException("Usage: JixooExport rgb-directory output-directory");
        Path destination = Path.of(args[1]);
        Files.createDirectories(destination);
        try (var paths = Files.list(Path.of(args[0]))) {
            for (Path source : paths.filter(p -> p.toString().endsWith(".rgb")).sorted().toList()) {
                byte[] raw = Files.readAllBytes(source);
                int stride = 64 * 64 * 3;
                if (raw.length == 0 || raw.length % stride != 0) throw new IllegalArgumentException("Invalid RGB file: " + source);
                var frames = new ArrayList<PixooFrame>();
                for (int offset=0; offset<raw.length; offset+=stride) {
                    frames.add(new PixooFrame(Arrays.copyOfRange(raw, offset, offset+stride), 80));
                }
                Path output = destination.resolve(source.getFileName().toString().replace(".rgb", ".gif"));
                GifEncoder.encode(new PixooAnimation(frames), output);
                System.out.println(output + " / " + frames.size() + " frames / " + Files.size(output) + " bytes");
            }
        }
    }
}
