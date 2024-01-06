import { execSync } from "child_process";

export function remarkModifiedTime() {
  return function (tree, file) {
    const filepath = file.history[0];
    const result = execSync(`git log -1 --pretty="format:%cI" "${filepath}"`);
    file.data.astro.frontmatter.lastModified = result.toString();
  };
}

export function remarkCreatedTime() {
  return function (tree, file) {
    const filepath = file.history[0];
    const result = execSync(`git log --reverse --pretty="format:%cI" "${filepath}" | head -1`);
    file.data.astro.frontmatter.date = result.toString();
  };
}